from consumeless import app, db
import datetime
import jwt

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deposit = db.Column(db.Numeric(), nullable=False)
    overdue_charge = db.Column(db.Numeric(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, default=True)
    owner = db.relationship("User", primaryjoin = "Item.owner_id == User.id", backref="owner")

    def __init__(self, name, description, category, owner_id, deposit, overdue_charge, created_at):
        self.name = name
        self.description = description
        self.category = category
        self.owner_id = owner_id
        self.deposit = deposit
        self.overdue_charge = overdue_charge
        self.created_at = created_at

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'owner_id': self.owner_id,
            'deposit': str(self.deposit),
            'overdue_charge': str(self.overdue_charge),
            'created_at': self.created_at.strftime("%d/%m/%Y")
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password_hash, created_at):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime("%d/%m/%Y")
        }

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
            'iat': datetime.datetime.utcnow(),
            'user_id': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    return_by = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    lender = db.relationship("User", primaryjoin = "Booking.owner_id == User.id", backref="lent_items")
    borrower = db.relationship("User", primaryjoin = "Booking.created_by == User.id", backref="borrowed_items")

    def __init__(self, item_id, owner_id, created_by, created_at, return_by):
        self.item_id = item_id
        self.owner_id = owner_id
        self.created_by = created_by
        self.created_at = created_at
        self.return_by = return_by

    def serialize(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'owner_id': self.owner_id,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'return_by': self.return_by,
            'confirmed': self.confirmed,
        }
