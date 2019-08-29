from collections import defaultdict
from .common import *

# Assigned to the full, absolute path at the beginning of each add/access call
tmp_fullpath = None

class Dispatcher:
    """
    Basically a router

    Can add routes and access the route
    """

    class RouteNode:
        def __init__(self):
            # A dict contiaining request method to the response
            # key: {GET, POST, PUT, DELETE}
            # value: response
            self.response = {
            }

            # A dict containing path to the RouteNode that handles that path
            # key: str
            # value: RouteNode
            self.routes = defaultdict(Dispatcher.RouteNode)

        @staticmethod
        def get_first_route_in_path(path):
            """
            Finds the first route in the given path
            For example, for inputs like "/user/id" or "user/id"，this returns ("user", "id) 

            :param path: a {relative, absolute} path like "/user/id" or "user/id"
            :type path: str
            :return: (the first route, the path but with first route removed)
            :rtype: (str, str)
            """
            path = path.strip()

            # remove leading & trailing /
            path = path.strip('/')

            if not path:
                return "", ""

            if '/' not in path:
                return path, ""

            idx = path.find('/')
            ret = path[:idx], path[idx + 1:]

            return ret

        def add(self, method, path, payload):

            cur, path = self.get_first_route_in_path(path)

            # end of recursion
            if cur == "":
                if method in self.response:
                    raise BadRequestException(f'Failed to add new route: route "{method} {tmp_fullpath}" already exists.')

                self.response[method] = payload
                return self

            self.routes[cur].add(method, path, payload)
            return self

        def access(self, method, path):
            """
            Always check current before recursively access next
            :param path:
            :type path: str
            :param full_path:
            :type full_path: str
            :return:
            :rtype:
            """
            cur, path = self.get_first_route_in_path(path)

            # end of recursion
            if cur == "":
                if method not in self.response:
                    raise BadRequestException(f'Invalid request method "{method} {tmp_fullpath}"')

                return self.response[method]

            if cur not in self.routes:
                raise BadRequestException(f'Invalid request path "{method} {tmp_fullpath}"')

            return self.routes[cur].access(method, path)

    def __init__(self):
        # key: path (str)
        # value: a dict containing response
        self.root_route = self.RouteNode()

    def set_fullpath(self, path):
        global tmp_fullpath
        tmp_fullpath = path
    
    def add(self, method, path, payload):
        """
        Add new route
        :param path:
        :type path: str
        :param payload:
        :type payload:
        :return: Success or not
        :rtype: bool
        """
        self.set_fullpath(path)
        self.root_route.add(method, path, payload)
        return True

    def access(self, method, path):
        """
        Access existing route

        :param path:
        :type path: str
        :return: the response
        :rtype: dict
        """
        self.set_fullpath(path)
        return self.root_route.access(method, path)
