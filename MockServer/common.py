class MockServerException(Exception):
    def __str__(self):
        return type(self).__name__ + ": " + super().__str__()

class BadRuleException(MockServerException):
    pass

class BadRequestException(MockServerException):
    pass

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"
METHODS_ALLOWED = [GET, POST, PUT, DELETE]