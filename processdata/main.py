import firebase_admin
from firebase_admin import firestore
import flask

app = flask.Flask(__name__)

firebase_admin.initialize_app()
SUPERHEROES = firestore.client().collection('muscledata')

@app.route('/processdata', methods=['POST'])
def create_hero():
    req = flask.request.json
    hero = SUPERHEROES.document()
    hero.set(req)
    return flask.jsonify({'id': hero.id}), 201

@app.route('/processdata/<id>')
def read_hero(id):
    return flask.jsonify(_ensure_hero(id).to_dict())

@app.route('/processdata/<id>', methods=['PUT'])
def update_hero(id):
    _ensure_hero(id)
    req = flask.request.json
    SUPERHEROES.document(id).set(req)
    return flask.jsonify({'success': True})

@app.route('/processdata/<id>', methods=['DELETE'])
def delete_hero(id):
    _ensure_hero(id)
    SUPERHEROES.document(id).delete()
    return flask.jsonify({'success': True})

def _ensure_hero(id):
    try:
        return SUPERHEROES.document(id).get()
    except:
        flask.abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
