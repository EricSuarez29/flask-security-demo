from flask_security import UserMixin, RoleMixin
from db import db

roles_users = db.Table(
        'roles_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users,
                                    backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sku = db.Column(db.String(10))
    name = db.Column(db.String(40))
    description = db.Column(db.Text())
    image = db.Column(db.String(255))
    price = db.Column(db.Double())

