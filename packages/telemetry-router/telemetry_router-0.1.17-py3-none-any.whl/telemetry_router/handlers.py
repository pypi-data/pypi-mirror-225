from requests import Session, Request
from ._version import __version__
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
import os, json, concurrent, tornado
import urllib.request

class RouteHandler(ExtensionHandlerMixin, JupyterHandler):

    executor = concurrent.futures.ThreadPoolExecutor(5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self, resource):
        try:
            self.set_header('Content-Type', 'application/json') 
            if resource == 'version':
                self.finish(json.dumps(__version__))
            elif resource == 'env':
                self.finish(json.dumps({
                    'workspaceID': os.getenv('WORKSPACE_ID') if os.getenv('WORKSPACE_ID') is not None else 'UNDEFINED'
                    }))
            else:
                self.set_status(404)
        except Exception as e:
            self.log.error(str(e))
            self.set_status(500)
            self.finish(json.dumps(str(e)))

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, resource):
        try:
            if resource == 'mongo':
                result = yield self.process_mongo_request()
                self.finish(json.dumps(result))
            elif resource == 's3':
                result = yield self.process_s3_request()
                self.finish(json.dumps(result))
            # elif resource == 'influx':
            #     result = yield self.process_influx_request()
            #     self.finish(json.dumps(result)) 
            else:
                self.set_status(404)

        except Exception as e:
            self.log.error(str(e))
            self.set_status(500)
            self.finish(json.dumps(str(e)))

    @tornado.concurrent.run_on_executor
    def process_mongo_request(self):
        log = json.loads(self.request.body)

        mongo_params = {
            'mongo_cluster': self.extensionapp.mongo_cluster,
            'mongo_db': self.extensionapp.mongo_db,
            'mongo_collection': self.extensionapp.mongo_collection,
        }

        data = json.dumps({
            'log': log,
            'mongo_params': mongo_params
        })

        with Session() as s:
            req = Request(
                'POST',
                self.extensionapp.api + "/mongo",
                data=data,
                headers={
                    'content-type': 'application/json'
                }
            )
            prepped = s.prepare_request(req)
            res = s.send(prepped, proxies=urllib.request.getproxies())
            return {
                'status_code': res.status_code,
                'reason': res.reason,
                'text': res.text
            }
        
    @tornado.concurrent.run_on_executor
    def process_s3_request(self):
        data = self.request.body

        with Session() as s:
            req = Request(
                'POST', 
                # self.extensionapp.api + "/s3",
                self.extensionapp.s3_url,
                data=data,
                headers={
                    'content-type': 'application/json'
                }
            )
            prepped = s.prepare_request(req)
            res = s.send(prepped, proxies=urllib.request.getproxies()) 
            return {
                'status_code': res.status_code,
                'reason': res.reason,
                'text': res.text
            }

    # @tornado.concurrent.run_on_executor
    # def process_influx_request(self):
    #     data = self.request.body

    #     with Session() as s:
    #         req = Request(
    #             'POST', 
    #             # self.extensionapp.api + "/influx",
    #             data=data,
    #             headers={
    #                 'content-type': 'application/json'
    #             }
    #         )
    #         prepped = s.prepare_request(req)
    #         res = s.send(prepped, proxies=urllib.request.getproxies()) 
    #         return {
    #             'status_code': res.status_code,
    #             'reason': res.reason,
    #             'text': res.text
    #         }