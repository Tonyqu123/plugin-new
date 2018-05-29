class APIException(Exception):
    def __init__(self, error_id, message, code=500):
        super(APIException, self).__init__(message)
        self.message = message
        self.error_id = error_id
        self.code = code


def job_name_duplicated(msg=''):
    raise APIException('jobs_name_duplicated_error', msg, 400)


def job_id_not_found(msg=''):
    raise APIException('job_id_not_found', msg, 404)


def executor_id_not_found(msg=''):
    raise APIException('executor_id_not_found', msg, 404)
