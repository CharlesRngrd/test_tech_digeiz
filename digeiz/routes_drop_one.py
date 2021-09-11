from flask import Flask, Blueprint, jsonify, make_response
from digeiz.models import Account, Mall, Unit
from digeiz import db


drop_one = Blueprint('drop_one', __name__)


@drop_one.route('/account/<id>', methods = ['DELETE'])
def account_drop(id):
    account = db.session.query(Account).get(id)

    if not account:
        return make_response(jsonify({'message': 'Account ID doesn\'t exists'}), 400)

    Account.query.filter_by(id=id).delete()
    Mall.query.filter_by(account_id=id).delete()
    Unit.query.filter_by(account_id=id).delete()
    db.session.commit()

    return make_response(jsonify({'message': 'Account deleted'}), 200)


@drop_one.route('/mall/<id>', methods = ['DELETE'])
def mall_drop(id):
    mall = db.session.query(Mall).get(id)

    if not mall:
        return make_response(jsonify({'message': 'Mall ID doesn\'t exists'}), 400)

    Mall.query.filter_by(id=id).delete()
    Unit.query.filter_by(mall_id=id).delete()
    db.session.commit()

    return make_response(jsonify({'message': 'Mall deleted'}), 200)


@drop_one.route('/unit/<id>', methods = ['DELETE'])
def unit_drop(id):
    unit = db.session.query(Unit).get(id)

    if not unit:
        return make_response(jsonify({'message': 'Unit ID doesn\'t exists'}), 400)

    Unit.query.filter_by(id=id).delete()
    db.session.commit()

    return make_response(jsonify({'message': 'Unit deleted'}), 200)
