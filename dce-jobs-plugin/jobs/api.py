import json
import datetime
from flask import Response
from flask_restful import Api, Resource, reqparse
from werkzeug.exceptions import HTTPException

from dce_client import require_auth
from error import APIException
from job import get_job
from job import get_jobs
from job import create_job
from job import modify_job
from job import delete_job
from job import start_job
from job import get_exec_history
from job import inspect_executor
from job import get_executor_container_output
from utils import from_view_dict


def error_message(error_id='', message=None):
    return Response(json.dumps({'id': error_id, 'message': message or error_id}, indent=4),
                    mimetype='application/json')


class JobApi(Api):
    def handle_error(self, e):
        if isinstance(e, APIException):
            return error_message(e.error_id, e.message), e.code
        if isinstance(e, HTTPException):
            return error_message('unknown_exception', str(e)), 400
        raise e


def load_api(app):
    api = JobApi(app)
    api.add_resource(JobsAPI, '/api/jobs')
    api.add_resource(JobsActionApi, '/api/jobs/<string:job_id>')
    api.add_resource(JobsStartApi, '/api/jobs/<string:job_id>/start')
    api.add_resource(JobsExecutorInspectApi, '/api/jobs/<string:job_id>/inspect/<string:executor_id>')
    api.add_resource(JobExecutorHistory, '/api/jobs/history')
    api.add_resource(JobLogDownloadApi, '/api/jobs/<string:job_id>/log/<string:executor_id>')


class JobsAPI(Resource):
    def get(self):
        args = reqparse.RequestParser(). \
            add_argument('AppName', required=False, default=None). \
            parse_args()
        args = from_view_dict(args)
        return [j.as_view_dict() for j in get_jobs(**args)]

    @require_auth
    def post(self):
        args = reqparse.RequestParser(). \
            add_argument('Name', required=True). \
            add_argument('AppName', required=True). \
            add_argument('ServiceName', required=False). \
            add_argument('Cmd', required=True). \
            add_argument('User'). \
            add_argument('Privileged', type=bool). \
            add_argument('Env', action='append', default=None). \
            add_argument('SecretArgs', action='append', default=None). \
            parse_args()
        args = from_view_dict(args)
        return create_job(**args).as_view_dict(), 201


class JobsActionApi(Resource):
    @require_auth
    def put(self, job_id):
        args = reqparse.RequestParser(). \
            add_argument('Name', required=True). \
            add_argument('AppName', required=True). \
            add_argument('ServiceName', required=True). \
            add_argument('Cmd', required=True). \
            add_argument('User'). \
            add_argument('Privileged', type=bool). \
            add_argument('Env', action='append', default=None). \
            add_argument('SecretArgs', action='append', default=None). \
            parse_args()
        args = from_view_dict(args)
        return modify_job(job_id=job_id, **args).as_view_dict()

    @require_auth
    def delete(self, job_id):
        return delete_job(job_id=job_id), 202


class JobsStartApi(Resource):
    @require_auth
    def post(self, job_id):
        args = reqparse.RequestParser(). \
            add_argument('Target', required=True, action='append', default=[], type=dict). \
            parse_args()
        args = from_view_dict(args)
        return start_job(job_id=job_id, **args).as_view_dict(), 201


class JobsExecutorInspectApi(Resource):
    def get(self, job_id, executor_id):
        return inspect_executor(job_id=job_id, executor_id=executor_id)


class JobExecutorHistory(Resource):
    def get(self):
        args = reqparse.RequestParser(). \
            add_argument('AppName', required=False, default=None). \
            add_argument('JobId', required=False, default=None). \
            parse_args()
        args = from_view_dict(args)
        executors = get_exec_history(**args)
        return executors


class JobLogDownloadApi(Resource):
    def get(self, job_id, executor_id):
        args = reqparse.RequestParser(). \
            add_argument('ContainerId', required=True, default=''). \
            parse_args()
        args = from_view_dict(args)
        container_id = args['container_id']
        job = get_job(job_id)
        if not job:
            return ''

        output, timestamp = get_executor_container_output(job_id, executor_id, container_id)
        headers = {
            'Content-Disposition': 'attachment; filename="job-container-{0}-{1}.log"'.format(
                container_id, datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d-%H:%M:%S')
            ),
            'Content-Type': 'text/plain'
        }
        return Response(
            output,
            mimetype='text/plain',
            headers=headers.iteritems())
