import os
from datetime import date
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
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

@app.route("/login", methods=["POST"])
def login_user():
    print(request.form)
    username=request.form.get('username')
    password=request.form.get('password')
    try:
        user=User.query.filter_by(username=username).first()
        if check_password_hash(user.password_hash, password):
            session.clear()
            session['user_id'] = user.id
            return "Well Done"
        else:
            return "invalid password"
    except Exception as e:
        return(str(e))

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

@app.route("/api/user/new", methods=["POST"])
def add_user():
    print(request.form)
    username=request.form.get('username')
    email=request.form.get('email')
    password_hash=generate_password_hash(request.form.get('password'))
    created_at=date.today().strftime("%d/%m/%Y")
    try:
        user=User(username = username,
                email = email,
                password_hash = password_hash,
                created_at = created_at,)
        db.session.add(user)
        db.session.commit()
        return f"successfully added user: {user.username}"
    except Exception as e:
        return(str(e))

api.add_resource(ApiItem, '/api/item/<i_id>')
api.add_resource(ApiUser, '/api/user/<u_id>')

if __name__ == '__main__':
    app.run()
