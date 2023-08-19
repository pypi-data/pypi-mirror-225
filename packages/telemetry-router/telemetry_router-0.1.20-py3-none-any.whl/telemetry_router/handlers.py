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
            if resource == 'export':
                result = yield self.export()
                self.finish(json.dumps(result))
            else:
                self.set_status(404)

        except Exception as e:
            self.log.error(str(e))
            self.set_status(500)
            self.finish(json.dumps(str(e)))

    @tornado.concurrent.run_on_executor
    def export(self):
        exporters = self.extensionapp.exporters
        requestBody = json.loads(self.request.body)
        result = []

        for exporter in exporters:
            data = {
                'data': requestBody,
                'params': exporter.get('params'), # none if exporter does not contain 'params'
                'env': [{x: os.getenv(x)} for x in exporter.get('env')] if (exporter.get('env')) else []
            }

            if (exporter.get('type') == 'console'):
                result.append({
                    'exporter': exporter.get('id'),
                    'message': data
                })

            elif (exporter.get('type') == 'file'):
                f = open(exporter.get('path'), 'a+', encoding='utf-8') # appending
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.write(',')
                f.close()
                result.append({
                    'exporter': exporter.get('id'),
                })

            elif (exporter.get('type') == 'remote'):
                with Session() as s:
                    request = Request(
                        'POST',
                        exporter.get('url'),
                        data=json.dumps(data),
                        headers={
                            'content-type': 'application/json'
                        }
                    )
                    prepped = s.prepare_request(request)
                    response = s.send(prepped, proxies=urllib.request.getproxies())
                result.append({
                    'exporter': exporter.get('id'),
                    'status_code': response.status_code,
                    'reason': response.reason,
                    'text': response.text
                })

        return result