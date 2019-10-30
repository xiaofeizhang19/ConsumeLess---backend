from app import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    deposit = db.Column(db.Numeric(precision=2), nullable=False)
    overdue_charge = db.Column(db.Numeric(precision=2), nullable=False)

    def __init__(self, name, description, category, email, deposit, overdue_charge):
        self.name = name
        self.description = description
        self.category = category
        self.email = email
        self.deposit = deposit
        self.overdue_charge = overdue_charge

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'email': self.email,
            'deposit': self.deposit,
            'overdue_charge': self.overdue_chargeß
        }
