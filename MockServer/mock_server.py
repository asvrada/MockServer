import json
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

from .dispatcher import Dispatcher
from .common import *

class MockServer:
    """
    MockServer
    """

    def __init__(self):
        ###
        # Decleration of variables
        ###
        # The Flask app instance
        self.app = Flask(__name__)
        CORS(self.app)

        # Map of entry and response
        self.dispatch = Dispatcher()

        ###
        # Other
        ###
        # Manually apply the app.route decorator
        # So self.flask_index can handle messages received sent to Flask server
        self.flask_index = self.app.route("/", defaults={'path': ""}, methods=METHODS_ALLOWED)(self.flask_index)
        self.flask_index = self.app.route("/<path:path>", methods=METHODS_ALLOWED)(self.flask_index)

    def run(self, port=5555):
        self.app.run(port=port)

    def flask_index(self, path):
        """
        Entry function for Flask application
        Try to fetch the correct payload and make a resposne
        """
        path = f"/{path}"
        method = request.method.upper()

        # print payload
        if request.data:
            print(">>>")
            print(json.loads(request.data))

        payload, code = None, 200

        try:
            payload = self.dispatch.access(method, path)
        except BadRequestException as e:
            payload = {
                'error': str(e)
            }
            code = 404

        if type(payload) is not str:
            payload = jsonify(payload)

        response = make_response(payload, code)
        
        response.headers['Content-Type'] = "application/json"
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

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
        :param method: {str} type of the request, one of METHODS_ALLOW
        :param path: {str} path to the endpoint
        :param status_code: {int} the status code of response
        :param body: {Any} the return body of response
        :param header: {dict} NOT USED
        """
        method = method.upper()

        try:
            if method not in METHODS_ALLOWED:
                raise BadRuleException(f"Invalid method '{method}', must be one of {METHODS_ALLOWED}")

            self.dispatch.add(method, path, body)
        except BadRuleException as e:
            return str(e)
