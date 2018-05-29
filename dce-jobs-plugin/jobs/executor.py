import etcd
import os
import time
import json
import sqlite3
import logging
import threading
from urlparse import urlparse

from config import DCE_JOBS_PLUGIN_LOG_STORE_PATH
from config import DCE_JOBS_PLUGIN_ETCD_URL
from docker_client import exec_create
from docker_client import exec_start
from docker_client import exec_inspect
from utils import to_view_dict
from utils import from_view_dict


log = logging.getLogger(__name__)
CLEAN_INTERVAL = 60 * 60 * 6

STATUS_STARTING = 'STARTING'
STATUS_CREATED = 'CREATED'
STATUS_CREATE_FAILED = 'CREATE_FAILED'
STATUS_RUNNING = 'RUNNING'
STATUS_RUNNING_FAILED = 'RUNNING_FAILED'
STATUS_FINISHED = 'FINISHED'


DB_NAME = os.path.join(DCE_JOBS_PLUGIN_LOG_STORE_PATH, 'dce-jobs-plugin.db')
ETCD_CLIENT = None


def etcd_client():
    if not DCE_JOBS_PLUGIN_ETCD_URL:
        return None

    global ETCD_CLIENT
    if not ETCD_CLIENT:
        c = etcd.Client(host=urlparse(DCE_JOBS_PLUGIN_ETCD_URL).hostname,
                        port=urlparse(DCE_JOBS_PLUGIN_ETCD_URL).port)
        try:
            c.store_stats()
        except:
            return None
        else:
            ETCD_CLIENT = c

    return ETCD_CLIENT


def exec_once(exe, is_insert=False):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    info = json.dumps(exe.as_dict())
    view_info = json.dumps(exe.as_view_dict())
    if is_insert:
        cur.execute("INSERT INTO executor (job_id, executor_id, info, view_info, app_name) VALUES (?, ?, ?, ?, ?)", (
            exe.job_id, exe.executor_id, info, view_info, exe.job.app_name
        ))
    else:
        cur.execute("UPDATE executor SET info=?, view_info=? WHERE job_id=? AND executor_id=?", (
            info, view_info, exe.job_id, exe.executor_id
        ))
    con.commit()
    cur.close()
    con.close()


def query_one(sql):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    try:
        cur.execute(sql)
        r = cur.fetchone()
        if not r:
            return None
        return r
    except Exception as e:
        log.error(e, exc_info=True)
        return None


def query_all(sql):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    try:
        cur.execute(sql)
        r = cur.fetchall()
        if not r:
            return []
        return r
    except Exception as e:
        log.error(e, exc_info=True)
        return []


class Executor(object):
    # TABLE_NAME = 'executor'
    def __init__(self, job, target):
        self.job = job
        self.job_id = job.job_id

        self.target = [from_view_dict(t) for t in target]
        self.result = []
        self.create_time = time.time()

        for t in self.target:
            node_id = t['node_id']
            container_id = t['container_id']
            self.result.append({
                'job_id': job.job_id,
                'job_name': job.name,
                'node_id': node_id,
                'container_id': container_id,
                'status': STATUS_STARTING,
                'start_time': 0,
                'end_time': 0
            })

        self.cmd = '{0} {1}'.format(job.cmd, ' '.join(job.secret_args))
        self.privileged = job.privileged
        self.user = job.user
        self.env = job.env

        self.save(is_insert=True)

    @property
    def executor_id(self):
        return str(int(self.create_time))

    @classmethod
    def new_instance(cls, job, target):
        executor = cls(job, target)
        run_daemon_thread(executor.do)
        return executor

    def do(self):
        log.info('@ Thread: {0}. Executor start with ID {1} jobID {2} targetNum {3}.'.format(
            threading.currentThread().ident, self.executor_id, self.job.job_id, len(self.target)))

        for t, r in zip(self.target, self.result):
            # JUST create
            try:
                node_id = t['node_id']
                container_id = t['container_id']

                exec_instance = exec_create(node_id, container_id, self.cmd, self.privileged, self.user, self.env)
                r['ID'] = exec_instance['Id']
                r['status'] = STATUS_CREATED

            except Exception as e:
                r['status'] = STATUS_CREATE_FAILED
                r['e'] = str(e)
            finally:
                r['start_time'] = time.time()
                from log import logger
                logger.debug('% r :{} %'.format(r))
                self.save()

        for t, r in zip(self.target, self.result):
            if not 'ID' in r:
                continue

            try:
                node_id = t['node_id']
                exec_id = r['ID']
                r['status'] = STATUS_RUNNING
                r['Output'] = exec_start(node_id, exec_id, stream=False)
                r.update(**exec_inspect(node_id, exec_id))
                r['status'] = STATUS_FINISHED
            except Exception as e:
                r['status'] = STATUS_RUNNING_FAILED
                r['e'] = str(e)
            finally:
                r['end_time'] = time.time()
                self.save()

        log.info('@ Thread: {0}. Executor end with ID {1} jobID {2} targetNum {3}.'.format(
            threading.currentThread().ident, self.executor_id, self.job.job_id, len(self.target)))

    def save(self, is_insert=False):
        exec_once(self, is_insert=is_insert)

    @classmethod
    def get_view_info_from_db(self, job_id, executor_id):
        sql = """select id, job_id, executor_id, info, view_info from executor where job_id='{job_id}' AND executor_id='{executor_id}'""".format(
            job_id=job_id,
            executor_id=executor_id
        )
        r = query_one(sql)
        if not r:
            return {}
        info = json.loads(r[4])
        return info

    @classmethod
    def get_info_from_db(self, job_id, executor_id):
        sql = """select id, job_id, executor_id, info, view_info from executor where job_id='{job_id}' AND executor_id='{executor_id}'""".format(
            job_id=job_id,
            executor_id=executor_id
        )

        r = query_one(sql)
        if not r:
            return {}
        info = json.loads(r[3])
        return info

    @classmethod
    def query_from_db(cls, job_ids):
        job_ids_s = ', '.join(["""'""" + j + """'""" for j in job_ids])
        sql = """select id, job_id, executor_id, info, view_info from executor where job_id IN ({job_ids_s})""".format(
            job_ids_s=job_ids_s
        )
        result = query_all(sql)
        return [json.loads(r[4]) for r in result]

    @classmethod
    def query_with_app_name(cls, app_name):
        sql = """select id, job_id, executor_id, info, view_info from executor where app_name = '{app_name}'""".format(
            app_name=app_name
        )
        result = query_all(sql)
        return [json.loads(r[4]) for r in result]

    @classmethod
    def query_all_id(cls):
        sql = '''select job_id, executor_id from executor'''
        result = query_all(sql)
        return result

    @staticmethod
    def init_db():
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        sql = '''create table executor (id INTEGER PRIMARY KEY autoincrement,
                                        job_id VARCHAR(40),
                                        executor_id VARCHAR(16),
                                        info TEXT,
                                        view_info TEXT,
                                        app_name VARCHAR(512))'''
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

    @staticmethod
    def delete_executor(job_id):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        sql = """delete from executor where job_id='{job_id}'""".format(job_id=job_id)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

    def as_dict(self):
        return dict(
            job_id=self.job_id,
            target=self.target,
            result=self.result,
            create_time=self.create_time
        )

    def as_view_dict(self):
        d = dict(
            job_id=self.job_id,
            target=[to_view_dict(t) for t in self.target],
            result=[to_view_dict(r) for r in self.result],
            create_time=self.create_time
        )
        return to_view_dict(d)

    def __str__(self):
        return '<Executor: {0} jobId: {1} targetNum: {2}>'.format(self.executor_id, self.job_id[:8], len(self.target))


def run_daemon_thread(target, *args, **kwargs):
    job_thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    job_thread.setDaemon(True)
    job_thread.start()


def get_executor(job_id, executor_id):
    return Executor.get_view_info_from_db(job_id, executor_id)


def query_executors(app_name):
    return Executor.query_with_app_name(app_name)


def get_output(job_id, executor_id, container_id):
    executor = Executor.get_info_from_db(job_id, executor_id)
    result = next((r for r in executor['result'] if r.get('container_id') == container_id), None)
    if not result:
        return ''

    if 'Output' in result:
        return result['Output'], result['start_time']
    else:
        return result.get('e', ''), result['start_time']


def delete_executor_history(job_id):
    Executor.delete_executor(job_id)
