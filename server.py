import json

from bottle import run, static_file, Bottle, JSONPlugin

from gene_ontology.obo import Value
from ontology import parse_obo


class ValueEncoder(json.JSONEncoder):
    "Extending the JSON encoder to handle OBO Values"
    def default(self, obj):
        if isinstance(obj, Value):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


app = Bottle()
app.install(JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=ValueEncoder)))


@app.route('/')
def staticindex():
    return static_file('index.html', root='ui')


@app.route('/static/<filepath:path>')
def staticpath(filepath):
    return static_file(filepath, root='ui')


@app.get('/ontology')
def get_ontology():
    obo = parse_obo("psoroto.obo")
    return dict(domain=obo["pso"], relation=obo["psro"],
                converse_domain=obo["roto"])


if __name__ == "__main__":
    run(app, host='', port=8081, debug=True, reloader=True)
