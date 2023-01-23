from ast import arg
import json

class RespHandler(object):
    def __init__(self, debug=False):
        self.debug = debug
        return
    
    def get_handler(self,respType,args=None):
        if self.debug and respType != "response_ok":
            print(f"ERROR: {respType} {args}")

        if hasattr(self,respType):
            if args is None:
                return getattr(self,respType)()
            return getattr(self, respType)(args)

        else:
            print(f"UNHANDLED RESPONSE TYPE: {respType}")
            return self.unhandled_error(str(args))
        
    def invalid_request(self, error):
        return json.dumps({"status":"Invalid Request","msg":error}), 400, {'ContentType': 'application/json'}

    def server_error(self,error):
        return json.dumps({"status":error}), 503, {'ContentType': 'application/json'}

    def unhandled_error(self, error):
        return json.dumps({"status":"Internal Server Error / Service Unavailable"}), 503, {'ContentType': 'application/json'}

    def unauthorized(self, error):
        return json.dumps({"status":"Unauthorized","msg":error}), 403, {'ContentType': 'application/json'}

    def forbidden(self, error):
        return json.dumps({"status":"Forbidden","msg":error}), 403, {'ContentType': 'application/json'}

    def token_auth(self):
        return json.dumps({"status":"Unauthorized","msg":"Incorrect Authorization (username or token)"}), 401, {'ContentType': 'application/json'}

    def rate_limit_exceeded(self):
        return json.dumps({"status":"Rate Limit Exceeded"}), 429, {'ContentType': 'application/json'}
    
    def not_found(self):
        return json.dumps({"status":"Not Found"}), 404, {'ContentType': 'application/json'}
    
    def response_ok(self, args={}):
        #if data in args:
        if "data" in args:
            data = json.dumps(args["data"],default=str)
            return data, 200, {'ContentType': 'application/json'}
        elif "msg" in args:
            msg = args["msg"]
            return json.dumps({"status":"OK","msg":msg}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({"status":"OK"}), 200, {'ContentType': 'application/json'}
    