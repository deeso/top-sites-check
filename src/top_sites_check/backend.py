from .topsites import ServiceInterface
from flask import Flask, jsonify


app = Flask(__name__)


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
