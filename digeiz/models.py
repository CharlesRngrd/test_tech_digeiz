from dataclasses import dataclass
from datetime import datetime
from digeiz import db


@dataclass
class Account(db.Model):
    id: int
    name: str
    creation_date: datetime
    malls: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    malls = db.relationship('Mall', backref=db.backref('account'))


@dataclass
class Mall(db.Model):
    id: int
    account_id: int
    name: str
    creation_date: datetime
    units: list
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    name = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    units = db.relationship('Unit', backref=db.backref('mall'))


@dataclass
class Unit(db.Model):
    id: int
    mall_id: int
    name: str
    creation_date: datetime
    
    id = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id'))
    name = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, default=datetime.now)
