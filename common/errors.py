from rest_framework.exceptions import APIException, ValidationError, NotFound


class ExternalAPIError(APIException):
    def __init__(self, detail=None, code=None):
        APIException.__init__(self, detail=None, code=None)
        if detail is None:
            self.detail = {'error_code': 1100, 'message': "External API has problems"}


class NoAtError(ValidationError):
    def __init__(self, detail=None, code=None):
        ValidationError.__init__(self, detail=None, code=None)
        if detail is None:
            self.detail = {'error_code': 1000, 'message': "No 'at' query param"}


class InvalidAtError(ValidationError):
    def __init__(self, detail=None, code=None):
        ValidationError.__init__(self, detail=None, code=None)
        if detail is None:
            self.detail = {'error_code': 1001, 'message': "'at' is not valid"}


class StationNotFoundError(NotFound):
    def __init__(self, detail=None, code=None):
        NotFound.__init__(self, detail=None, code=None)
        if detail is None:
            self.detail = {'error_code': 1002, 'message': 'Station not found'}


class WeatherNotFoundError(NotFound):
    def __init__(self, detail=None, code=None):
        NotFound.__init__(self, detail=None, code=None)
        if detail is None:
            self.detail = {'error_code': 1003, 'message': 'Weather not found'}
