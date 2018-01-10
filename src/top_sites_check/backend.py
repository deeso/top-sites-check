from werkzeug.serving import make_server
from flask import Flask
from threading import Thread

from .interface import ServiceInterface
from .logger import debug
from .consts import DATA_SOURCES, NAME


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
            debug("Adding rule:%s as (%s)" % (rule, endpoint))
            self.app.add_url_rule(rule, endpoint=endpoint,
                                  view_func=view_func, methods=methods)

        self.srv = make_server(self.host, self.port, self.app)
        self.thread = Thread(target=self.run_app, args=(self))
        _params = (self.name, self.host, self.port)
        debug("Starting server (%s) in thread: %s:%s" % _params)
        self.thread.start()

    def stop(self):
        if self.srv is not None:
            debug("Stopping server (%s)" % (self.name))
            self.srv.shutdown()
            self.thread.join()

    def run_app(self):
        debug("Running the app server (%s) in an infinite loop " % (self.name))
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
        debug("Updating server (%s) sources " % (self.name))
        for s in self.sources:
            s.update()

    def load(self, **kargs):
        debug("Loading server (%s) sources " % (self.name))
        for s in self.sources:
            s.load()

    def check(self, domain, **kargs):
        debug("Checking server (%s) sources for %s" % (self.name, domain))
        results = {}
        for s in self.sources:
            results.update(s.check(domain))

    def start(self):
        debug("Starting service (%s)" % (self.name))
        self.server.start()

    def stop(self):
        debug("Stopping service (%s)" % (self.name))
        self.server.stop()

    @classmethod
    def parse_toml(cls, toml_dict):
        ts_block = toml_dict[NAME] if NAME in toml_dict else toml_dict
        sources_blocks = ts_block.get('sources', {})
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
        kargs['host'] = ts_block.get('host', HOST)
        kargs['port'] = ts_block.get('port', PORT)
        kargs['name'] = ts_block.get('name', 'not specified')
        return cls(**kargs)
