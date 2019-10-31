import os
from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Item


class CrudItem(Resource):
    def get(self, id_):
        try:
            item=Item.query.filter_by(id=id_).first()
            return jsonify(item.serialize())
        except Exception as e:
            return(str(e))

@app.route("/")
def reroute_index():
    return redirect(url_for('get_all_items'))

@app.route("/api/item/index")
def get_all_items():
    try :
        items=Item.query.all()
        return jsonify([e.serialize() for e in items])
    except Exception as e:
        return(str())

api.add_resource(CrudItem, '/api/item/<id_>')

if __name__ == '__main__':
    app.run()
