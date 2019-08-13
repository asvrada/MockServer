from collections import defaultdict
from .common import BadRouteException


class Dispatcher:
    """
    Basically a router

    Can add routes and access the route
    """

    class RouteNode:
        def __init__(self):
            self.has_response = False
            self.response = {
                "get": None,
                "post": None,
                "put": None,
                "delete": None
            }

            # key: str
            # value: RouteNode
            self.routes = defaultdict(Dispatcher.RouteNode)

        @staticmethod
        def get_first_route_in_path(path):
            """
            Finds the first route in the given path
            For example, first route in "/user/id" or "user/id" is "user", and this function returns "id"

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

            # Throw error
            if ret[0] == "" and ret[1] != "":
                raise BadRouteException(f"Error when parsing path: {path}")

            return ret

        def add(self, path, payload):
            cur, path = self.get_first_route_in_path(path)

            if cur == "":
                # end of recursion
                self.has_response = True
                self.response = payload
                return self

            self.routes[cur].add(path, payload)
            return self

        def access(self, path, full_path):
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

            if cur == "":
                # end of recursion
                if not self.has_response:
                    raise BadRouteException(f"Invalid path: {full_path}")

                return self.response

            if cur not in self.routes:
                raise BadRouteException(f"Invalid path: {full_path}")

            return self.routes[cur].access(path, full_path)

    def __init__(self):
        # key: path (str)
        # value: a dict containing response
        self.root_route = self.RouteNode()

    def add(self, path, payload):
        """
        Add new route
        :param path:
        :type path: str
        :param payload:
        :type payload:
        :return: Success or not
        :rtype: bool
        """
        self.root_route.add(path, payload)
        return True

    def access(self, path):
        """
        Access existing route

        :param path:
        :type path: str
        :return: the response
        :rtype: dict
        """
        return self.root_route.access(path, path)
