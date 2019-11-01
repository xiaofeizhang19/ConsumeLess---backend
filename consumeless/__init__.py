import os
from datetime import date
from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Item, User

# using flask-restful to encompass crud for a single route
class ApiItem(Resource):
    def get(self, i_id):
        try:
            item=Item.query.filter_by(id=i_id).first()
            return jsonify(item.serialize())
        except Exception as e:
            return(str(e))

class ApiUser(Resource):
    def get(self, u_id):
        try:
            user=User.query.filter_by(id=u_id).first()
            return jsonify(user.serialize())
        except Exception as e:
            return(str(e))

@app.route("/")
def reroute_index():
    return redirect(url_for('get_all_items'))

@app.route("/api/item/new", methods=["POST"])
def add_item():
    print(request.form)
    name=request.form.get('name')
    description=request.form.get('description')
    category=request.form.get('category')
    email=request.form.get('email')
    deposit=request.form.get('deposit')
    overdue_charge=request.form.get('overdue_charge')
    created_at=date.today().strftime("%d/%m/%Y")
    try:
        item=Item(name = name,
                description = description,
                category = category,
                email = email,
                deposit = deposit,
                overdue_charge = overdue_charge,
                created_at = created_at,)
        db.session.add(item)
        db.session.commit()
        return f"successfully added item: {item.name}"
    except Exception as e:
        return(str(e))

@app.route("/api/item/index")
def get_all_items():
    try :
        items=Item.query.all()
        return jsonify([e.serialize() for e in items])
    except Exception as e:
        return(str())

api.add_resource(ApiItem, '/api/item/<i_id>')
api.add_resource(ApiUser, '/api/user/<u_id>')

if __name__ == '__main__':
    app.run()
