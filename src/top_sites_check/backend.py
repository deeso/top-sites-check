from werkzeug.serving import make_server

from .topsites import ServiceInterface
from flask import Flask, jsonify
from threading import Thread


class FlaskServer(object):
    def __init__(self, name, host='127.0.0.1', port=9006):
        self.port = port
        self.host = host
        self.running = False
        self.app = None
        self.thread = None
        self.name = name
        self.srv = None

    def start(self):
        self.app = Flask(self.name)
        self.srv = make_server(self.host, self.port, self.app)
        self.thread = Thread(target=self.run_app, args=(self))
        self.thread.start()

    def stop(self):
        if self.srv is not None:
            self.srv.shutdown()

    def run_app(self):
        self.srv.serve_forever()


@app.route('/topsites/update', methods=['GET'])
def handle_update_request():
    return jsonify({'tasks': {}})


@app.route('/topsites/check', methods=['GET'])
def handle_check_request():
    return jsonify({'tasks': {}})


@app.route('/topsites/load', methods=['GET'])
def handle_load_request():
    return jsonify({'tasks': {}})


class QueryService(ServiceInterface):
    def __init__(self, sources=[], **kargs):
            super(ServiceInterface, self).__init__(**kargs)
            self.sources = sources

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
