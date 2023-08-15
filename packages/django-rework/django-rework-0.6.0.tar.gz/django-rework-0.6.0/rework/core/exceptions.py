from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class ValidateError(APIException):
    status_code = 400
    default_detail = 'Request validate error.'
    default_code = 'validate_error'

    def __init__(self, detail=None, code=None, errors=None):
        self.errors = errors
        super().__init__(detail, code)

