from flask import Flask, request, make_response
from .dispatcher import Dispatcher
from .common import *

class MockServer:
    """
    MockServer
    """
    METHODS_ALLOWED = [GET, POST, PUT, DELETE]

    def __init__(self):
        ###
        # Decleration of variables
        ###
        # The Flask app instance
        self.app = Flask(__name__)

        # Map of entry and response
        self.dispatch = Dispatcher()

        ###
        # Other
        ###
        # Manually apply the app.route decorator
        # So self.flask_index can handle messages received sent to Flask server
        self.flask_index = self.app.route("/", defaults={'path': ""}, methods=self.METHODS_ALLOWED)(self.flask_index)
        self.flask_index = self.app.route("/<path:path>", methods=self.METHODS_ALLOWED)(self.flask_index)

    def run(self, port=5555):
        self.app.run(port=port)

    def flask_index(self, path):
        """
        Entry function for Flask application
        """
        path = f"/{path}"
        method = request.method.upper()
        return self.dispatch.access(method, path)

    def get(self, path, **arg):
        return self.when(GET, path, **arg)

    def post(self, path, **arg):
        return self.when(POST, path, **arg)

    def put(self, path, **arg):
        return self.when(PUT, path, **arg)

    def delete(self, path, **arg):
        return self.when(DELETE, path, **arg)

    def when(self, method, path, status_code=200, body="Default response: MockServer is running", header=None):
        """
        Store the response {method, path}: {status_code, body, header}
        """
        method = method.upper()

        if method not in [GET, POST, PUT, DELETE]:
            raise BadRouteException(f"Invalid method '{method}', must be one of {[GET, POST, PUT, DELETE]}")

        self.dispatch.add(method, path, body)
