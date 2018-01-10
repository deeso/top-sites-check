from werkzeug.serving import make_server
from .interface import ServiceInterface
from flask import Flask
from threading import Thread

from top_sites_check import DATA_SOURCES

HOST = '127.0.0.1'
PORT = 9006


class FlaskServer(object):

    def __init__(self, name, host=HOST, port=PORT, routes=[]):
        self.port = port
        self.host = host
        self.running = False
        self.app = None
        self.thread = None
        self.name = name
        self.srv = None
        self.routes = {}

    def start(self):
        self.app = Flask(self.name)
        for route in self.routes:
            rule = route['url']
            endpoint = route['endpoint']
            view_func = route['view_function']
            methods = route['methods']
            self.app.add_url_rule(rule, endpoint=endpoint,
                                  view_func=view_func, methods=methods)

        self.srv = make_server(self.host, self.port, self.app)
        self.thread = Thread(target=self.run_app, args=(self))
        self.thread.start()

    def stop(self):
        if self.srv is not None:
            self.srv.shutdown()

    def run_app(self):
        self.srv.serve_forever()


class QueryService(ServiceInterface):
    HOST = '127.0.0.1'
    PORT = 9006

    def __init__(self, sources=[], host=HOST, port=PORT, **kargs):
            super(ServiceInterface, self).__init__(**kargs)
            self.sources = sources
            self.routes = [
                {'rule': "/topsites/update",
                 "endpoint": "update",
                 "view_func": self.update,
                 "methods": ['GET'],
                 },
                {'rule': "/topsites/load",
                 "endpoint": "load",
                 "view_func": self.load,
                 "methods": ['GET'],
                 },
                {'rule': "/topsites/check",
                 "endpoint": "check",
                 "view_func": self.check,
                 "methods": ['GET'],
                 },
            ]
            self.name = kargs.get('name', '')
            self.server = FlaskServer(self.name, host=host, port=port,
                                      routes=self.routes, **kargs)

    def update(self, **kargs):
        for s in self.sources:
            s.update()

    def load(self, **kargs):
        for s in self.sources:
            s.load()

    def check(self, domain, **kargs):
        results = {}
        for s in self.sources:
            results.update(s.check(domain))

    @classmethod
    def parse_toml(cls, toml_dict):
        sources_blocks = toml_dict.get('sources', {})
        if len(sources_blocks) == 0:
            raise Exception("One or more data sources must be specified")

        sources = []
        for block in sources_blocks:
            bt = block.get('type', None)
            if bt is None or bt not in DATA_SOURCES:
                raise Exception("Source type is not valid or unknown: %s" % bt)
            b_cls = DATA_SOURCES.get(bt)
            source = b_cls.parse_toml(block)
            sources.append(source)

        kargs = {'sources': sources}
        kargs['host'] = toml_dict.get('host', HOST)
        kargs['port'] = toml_dict.get('port', PORT)
        kargs['name'] = toml_dict.get('name', 'not specified')

        return cls(**kargs)
