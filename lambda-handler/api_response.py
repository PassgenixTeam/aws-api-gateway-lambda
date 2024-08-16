import json

"""
This module defines classes for generating API responses.
Version: 2.0

Classes:
- Ok: Represents a successful API response.
- BaseException: Base class for API exceptions.
- NotFound: Represents a 404 Not Found exception.
- MethodNotAllowed: Represents a 405 Method Not Allowed exception.
- InternalServerError: Represents a 500 Internal Server Error exception.
"""


class Ok:
    def __init__(
        self, body, headers={"Content-Type": "application/json"}, is_json=True
    ):
        self.body = body
        self.headers = headers
        self.is_json = is_json

    def get_response(self):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": self.headers,
            "cookies": [],
            "body": json.dumps(self.body) if self.is_json else self.body,
        }


class Redirect:
    def __init__(self, location, body=""):
        self.location = location
        self.body = body

    def get_response(self):
        return {
            "isBase64Encoded": False,
            "statusCode": 302,
            "headers": {"Location": self.location},
            "cookies": [],
            "body": json.dumps(self.body),
        }


class BaseException(Exception):
    def get_response(self, fallback_message="An error occurred."):
        return {
            "isBase64Encoded": False,
            # "statusCode": ???, # Implement this in the child classes
            "headers": {"Content-Type": "application/json"},
            "cookies": [],
            "body": json.dumps(
                {
                    "message": str(self) or fallback_message,
                }
            ),
        }


class NotFound(BaseException):
    pass

    def get_response(self):
        response = super().get_response("Not found.")
        response["statusCode"] = 404
        return response


class MethodNotAllowed(BaseException):
    pass

    def get_response(self):
        response = super().get_response("Method not allowed.")
        response["statusCode"] = 405
        return response


class InternalServerError(BaseException):
    pass

    def get_response(self):
        response = super().get_response("Internal server error.")
        response["statusCode"] = 500
        return response
