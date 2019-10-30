import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Item

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/item/<id_>")
def get_item(id_):
    try:
        item=Item.query.filter_by(id=id_).first()
        return jsonify(item.serialize())
    except Exception as e:
        return(str(e))


if __name__ == '__main__':
    app.run()
