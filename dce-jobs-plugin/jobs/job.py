# encoding=utf-8
import uuid
import logging
from flask import g

from dce_job import SUCCEED
from dce_job import create_plugin_job
from error import job_name_duplicated
from error import job_id_not_found
from error import executor_id_not_found
from executor import Executor
from executor import get_executor
from executor import query_executors
from executor import get_output
from executor import delete_executor_history
from utils import to_view_dict
from storage import get_config
from storage import set_config
from storage import synchronous


log = logging.getLogger(__name__)


class Job(object):
    """

    """
    def __init__(self, job_id, app_name, service_name, name, cmd, privileged=False, user=None, env=None, executors=None,
                 secret_args=None):
        self.service_name = service_name
        self.app_name = app_name
        self.name = name
        self.cmd = cmd
        self.privileged = privileged
        self.user = user
        self.env = env or []
        self.executors = executors if executors is not None else []
        self.secret_args = secret_args if secret_args is not None else []

        self.job_id = job_id

        # unused yet
        # self.attach_stdin = attach_stdin
        # self.attach_stdout = attach_stdout
        # self.attach_stderr = attach_stderr
        # self.detach_keys = detach_keys
        # self.tty = tty

    @property
    def job_name(self):
        return '{0}-{1}'.format(self.app_name, self.name)

    def exec_once(self, target):
        """
        target: [
            {
                "ContainerId": "xxx",
                "NodeId": "yyy"
            },
            ......
        ]
        """
        e = Executor.new_instance(self, target)
        self.executors.append(e.executor_id)

    def as_dict(self, with_secret_args=False, with_executors=True):
        d = dict(
            job_id=self.job_id,
            app_name=self.app_name,
            service_name=self.service_name,
            name=self.name,
            cmd=self.cmd,
            privileged=self.privileged,
            user=self.user,
            env=self.env,
            # executors=self.executors,
            secret_args=self.secret_args if with_secret_args else ['*' * len(i) for i in self.secret_args]
        )
        if with_executors:
            d['executors'] = self.executors
        return d

    def as_view_dict(self):
        return to_view_dict(self.as_dict())

    @classmethod
    def new_instance(cls, app_name, service_name, name, cmd, privileged, user, env, secret_args=None):
        job_id = str(uuid.uuid4())
        return cls(job_id, app_name, service_name, name, cmd, privileged, user, env, secret_args=secret_args)

    @classmethod
    def from_data(cls, job_id, app_name, service_name, name, cmd, privileged, user, env, executors=None, secret_args=None):
        return cls(job_id, app_name, service_name, name, cmd, privileged, user, env, executors=executors, secret_args=secret_args)

    def __str__(self):
        return '<Job: {0}>'.format(self.job_name)


class Settings(object):
    def __init__(self):
        config = get_config()
        self.jobs = [Job.from_data(**j) for j in config['jobs']]
        result = Executor.query_all_id()
        for job in self.jobs:
            for r in result:
                if r[0] == job.job_id:
                    job.executors.append(r[1])

    def create_job(self, app_name, service_name, name, cmd, privileged=False, user=None, env=None, secret_args=None):
        if self.filter_out_jobs(app_name=app_name, name=name):
            return job_name_duplicated(name)

        env = env or []
        secret_args = secret_args or []
        job = Job.new_instance(app_name, service_name, name, cmd, privileged, user, env, secret_args=secret_args)
        self.jobs.append(job)
        self.save()
        return job

    def update_job(self, job_id, app_name, service_name, name, cmd, privileged=False, user='', env=None, secret_args=None):
        job = next((j for j in self.filter_out_jobs(job_id=job_id)), None)
        if not job:
            return job_id_not_found(job_id)

        job.app_name = app_name
        job.service_name = service_name
        job.name = name
        job.cmd = cmd
        job.privileged = privileged
        job.user = user
        job.env = env if env is not None else []

        secret_args = secret_args or []
        if '*' * len(''.join(secret_args)) != ''.join(secret_args):
            # if secret_args is not ['*', '**', '***']
            job.secret_args = secret_args if secret_args is not None else []

        self.save()
        return job

    def delete_job(self, job_id):
        job = next((j for j in self.filter_out_jobs(job_id=job_id)), None)
        if not job:
            return job_id_not_found(job_id)

        self.jobs = [j for j in self.jobs if j.job_id != job_id]
        self.save()

        # delete_executor_history(job_id)
        return job

    def start_job(self, job_id, target):
        job = next((j for j in self.filter_out_jobs(job_id=job_id)), None)
        if not job:
            return job_id_not_found(job_id)

        job.exec_once(target)
        self.save()
        return job

    def inspect_executor(self, job_id, executor_id):
        job = next((j for j in self.filter_out_jobs(job_id=job_id)), None)
        if not job:
            return job_id_not_found(job_id)

        executor = get_executor(job_id, executor_id)
        if not executor:
            return executor_id_not_found(executor_id)

        return executor

    def save(self):
        config = {
            'jobs': [j.as_dict(with_secret_args=True, with_executors=False) for j in self.jobs]
        }
        set_config(config)

    def filter_out_jobs(self, job_id=None, app_name=None, name=None):
        jobs = self.jobs

        if job_id is not None:
            jobs = [j for j in jobs if j.job_id == job_id]

        if app_name is not None:
            jobs = [j for j in jobs if j.app_name == app_name]

        if name is not None:
            jobs = [j for j in jobs if j.name == name]

        return jobs


def get_job(job_id):
    setting = Settings()
    jobs = setting.filter_out_jobs(job_id=job_id)
    if jobs:
        return jobs[0]
    return None


def get_jobs(app_name=None):
    setting = Settings()
    jobs = setting.filter_out_jobs(app_name=app_name)
    return jobs


@synchronous
def create_job(app_name, service_name, name, cmd, privileged, user, env, secret_args):
    setting = Settings()
    job = setting.create_job(app_name, service_name, name, cmd, privileged, user, env, secret_args)

    create_plugin_job('新建作业', g.username, SUCCEED, name)
    return job


@synchronous
def modify_job(job_id, app_name, service_name, name, cmd, privileged, user, env, secret_args):
    setting = Settings()
    job = setting.update_job(job_id, app_name, service_name, name, cmd, privileged, user, env, secret_args)

    create_plugin_job('修改作业', g.username, SUCCEED, name)
    return job


@synchronous
def delete_job(job_id):
    setting = Settings()
    job = setting.delete_job(job_id)

    create_plugin_job('删除作业', g.username, SUCCEED, job.name)
    return ''


@synchronous
def start_job(job_id, target):
    setting = Settings()
    job = setting.start_job(job_id, target)

    create_plugin_job('执行作业', g.username, SUCCEED, job.name)
    return job


def inspect_executor(job_id, executor_id):
    setting = Settings()
    return setting.inspect_executor(job_id, executor_id)


def get_exec_history(app_name=None, job_id=None):
    # setting = Settings()
    # jobs = setting.filter_out_jobs(job_id=job_id, app_name=app_name)
    executors = query_executors(app_name)
    return executors


def get_executor_container_output(job_id, executor_id, container_id):
    return get_output(job_id, executor_id, container_id)
