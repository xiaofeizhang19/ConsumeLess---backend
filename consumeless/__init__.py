import os
from datetime import date, datetime
import jwt
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
from functools import wraps
import requests
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
API_KEY = os.environ['GOOGLE_API_KEY']

from models import Item, User, Booking

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return error(403, "Token is missing!")
        try:
            token_data = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms='HS256')
        except:
            return error(407, "Token is invalid!")

        return f(token_data, *args, **kwargs)
    return decorated

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

@app.route("/api/item/index")
def get_all_items():
    items=Item.query.all()
    return jsonify([e.serialize() for e in items])

@app.route("/api/items")
@token_required
def get_all_my_items(token_data):
    owner_id = token_data['user_id']
    items=Item.query.filter_by(owner_id=owner_id).all()
    return jsonify([e.serialize() for e in items])

class ApiItem(Resource):
    def get(self, i_id):
        item = Item.query.filter_by(id=i_id).first()
        if item is None:
            return error(404, "Item not found")

        return jsonify(item.serialize())

    @token_required
    def post(token_data, self, i_id):
        name=request.form.get('name')
        description=request.form.get('description')
        category=request.form.get('category')
        owner_id=token_data['user_id']
        deposit=request.form.get('deposit')
        overdue_charge=request.form.get('overdue_charge')
        created_at=date.today().strftime("%d/%m/%Y")
        item=Item(name = name,
                description = description,
                category = category,
                owner_id = owner_id,
                deposit = deposit,
                overdue_charge = overdue_charge,
                created_at = created_at,)
        db.session.add(item)
        db.session.commit()
        return jsonify(
            message=f"successfully added item: {item.name}"
        )

class ApiUser(Resource):
    def get(self, u_id):
        user = User.query.filter_by(id=u_id).first()
        if user is None:
            return error(404, "User not found")

        return jsonify(user.serialize())

    def post(self, u_id):
        username=request.form.get('username')
        email=request.form.get('email')
        password_hash=generate_password_hash(request.form.get('password'))
        created_at=date.today().strftime("%d/%m/%Y")
        postcode=request.form.get('postcode')
        long_lat = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?components=country:GB|postal_code:ox26sq&key={API_KEY}')
        latitude = json.loads(long_lat.content)['results'][0]['geometry']['location']['lat']
        longitude = json.loads(long_lat.content)['results'][0]['geometry']['location']['lng']
        try:
            user=User(username = username,
                    email = email,
                    password_hash = password_hash,
                    created_at = created_at,
                    postcode = postcode,
                    latitude = latitude,
                    longitude = longitude)
            db.session.add(user)
            db.session.commit()
            token = (repr(user.encode_auth_token(user.id))[2:-1])
            return jsonify({'message': f"successfully added user: {user.username}", 'token' : str(token)})
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                abort(error(409, "User exists"))
            else:
                raise

@app.route("/api/bookings")
@token_required
def get_all_my_bookings(token_data):
    created_by = token_data['user_id']
    bookings=Booking.query.filter_by(created_by=created_by, confirmed=True).all()
    return jsonify([e.serialize() for e in bookings])

class ApiBooking(Resource):
    @token_required
    def get(token_data, self, b_id):
        if b_id == 'requests':
            confirmed = False
        else:
            confirmed = True
        owner_id = token_data['user_id']
        bookings = Booking.query.filter_by(owner_id=owner_id, confirmed=confirmed).all()
        return jsonify([e.serialize() for e in bookings])


    @token_required
    def post(token_data, self, b_id):
        item_id=request.form.get('item_id')
        owner_id=Item.query.with_entities(Item.owner_id).filter_by(id=item_id).first()[0]
        created_by=token_data['user_id']
        created_at=date.today()
        return_by=request.form.get('return_by')
        booking=Booking(item_id = item_id,
                owner_id = owner_id,
                created_by = created_by,
                created_at = created_at,
                return_by = return_by)
        db.session.add(booking)
        db.session.commit()
        return jsonify(f'{booking.return_by}')

    @token_required
    def patch(token_data, self, b_id):
        booking = Booking.query.filter_by(id=b_id).first()
        booking.confirmed = True
        db.session.commit()
        return jsonify(f'Booking {booking.id} confirmed successfully')

    @token_required
    def delete(token_data, self, b_id):
        booking = Booking.query.filter_by(id=b_id).first()
        db.session.delete(booking)
        db.session.commit()
        return jsonify(f'Booking deleted')

@app.route("/")
def reroute_index():
    return redirect(url_for('get_all_items'))

@app.route("/login", methods=["POST"])
def login_user():
    username=request.form.get('username')
    password=request.form.get('password')

    if not username or not password:
        abort(error(400, "Insufficient information"))

    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(error(400, "User does not exist"))

    if check_password_hash(user.password_hash, password):
        session.clear()
        session['user_id'] = user.id
        token = (repr(user.encode_auth_token(user.id))[2:-1])
        return jsonify({'message': f"successfully logged in user: {user.username}", 'token' : str(token)})

    abort(error(400, "Invalid password"))

@app.route("/api/categories/<cat>")
def get_items_by_category(cat):
    items = Item.query.filter_by(category=cat).all()
    return jsonify([e.serialize() for e in items])

api.add_resource(ApiItem, '/api/item/<i_id>')
api.add_resource(ApiUser, '/api/user/<u_id>')
api.add_resource(ApiBooking, '/api/booking/<b_id>')

# if __name__ == '__main__':
#     app.run()
