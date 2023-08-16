import json
import logging
import base64
class Response:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = json.dumps(body)
        
class Route:
    def __init__(self, path, http_methods=None):
        self.path = path
        self.http_methods = http_methods or ['GET']
        self.handlers = {}
        self.middleware_chain = []

    def use_middleware(self, middleware):
        if not callable(middleware):
            raise ValueError("Middleware must be callable")
        self.middleware_chain.append(middleware)

    def route(self, http_method, func):
        self.handlers[http_method] = func

    def handle_request(self, method, req_params):
        for middleware in self.middleware_chain:
            req_params = middleware(req_params)

        if method in self.handlers:
            handler = self.handlers[method]
            return handler(req_params)
        else:
            return Response(405, 'Method Not Allowed')

class Middleware:
    def __init__(self, process_request=None, process_response=None):
        self.process_request = process_request
        self.process_response = process_response

class LambdaFlask:
    def __init__(self, enable_request_logging=True, enable_response_logging=True):
        self.routes = {}
        self.enable_request_logging = enable_request_logging
        self.enable_response_logging = enable_response_logging
        self.logger = logging.getLogger(__name__)

    def route(self, path, http_methods=None):
        route = Route(path, http_methods)
        self.routes[path] = route
        return route

    def process_request(self, event):
        response = Response(500, 'Unable To Process Request')
        try:
            req_path = event['requestContext']['http']['path']
            method = event['requestContext']['http']['method']
            req_params = self.aggregate_params(event)

            if self.enable_request_logging:
                self.log_request(method, req_path, req_params)

            if req_path in self.routes:
                route = self.routes[req_path]
                response = route.handle_request(method, req_params)
            else:
                response = Response(404, 'Route Not Found')
        except Exception as e:
            response = Response(500, {'error': str(e)})

        if self.enable_response_logging:
            self.log_response(response)
        return Response(response.status_code, response.body)   
    def execute_handler(self, handler, req_params):
        return handler(req_params)
    def aggregate_params(self, event):
        query_params = event.get('queryStringParameters', {})
        body = event.get('body', {})
        if body and event.get('isBase64Encoded', False):
            body = json.loads(base64.b64decode(body).decode('utf-8'))
        elif body:
            body = json.loads(body)
        params = {**query_params, **body}
        return params
    def log_request(self, method, path, params):
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info("Request - Method: %s, Path: %s, Params: %s", method, path, params)

    def log_response(self, response):
        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info("Response - Status Code: %s, Body: %s", response['statusCode'], response['body'])


