import os
from datetime import date
from flask import (
    abort,
    Flask,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Item, User

def error(
    status=500,
    message="Internal Server Error"
):
    """Build an error response"""
    return make_response(
        jsonify(error=message),
        status,
    )


def handle_exception(e):
    """Default exception handler

    Any exceptions raised inside a route that we do not explicitly
    catch will be passed to this function and the we log them
    server side for debugging and return a generic internal server
    error to the client.
    """
    print(e)
    return error()

app.handle_exception = handle_exception


# using flask-restful to encompass crud for a single route
class ApiItem(Resource):
    def get(self, i_id):
        item=Item.query.filter_by(id=i_id).first()
        return jsonify(item.serialize())

class ApiUser(Resource):
    def get(self, u_id):
        user=User.query.filter_by(id=u_id).first()
        return jsonify(user.serialize())

@app.route("/")
def reroute_index():
    return redirect(url_for('get_all_items'))

@app.route("/login", methods=["POST"])
def login_user():
    print(request.form)
    username=request.form.get('username')
    password=request.form.get('password')
    user=User.query.filter_by(username=username).first()

    if check_password_hash(user.password_hash, password):
        session.clear()
        session['user_id'] = user.id
        return "Well Done"

    abort(error(400, "Invalid password"))

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

@app.route("/api/item/index")
def get_all_items():
    items=Item.query.all()
    return jsonify([e.serialize() for e in items])

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
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            abort(error(409, "User exists"))
        else:
            raise

api.add_resource(ApiItem, '/api/item/<i_id>')
api.add_resource(ApiUser, '/api/user/<u_id>')

if __name__ == '__main__':
    app.run()
