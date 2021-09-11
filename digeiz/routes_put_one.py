from flask import Blueprint, jsonify, make_response, request

from digeiz import db
from digeiz.models import Account, Mall, Unit

put_one = Blueprint('put_one', __name__)


# FIXME : return an error if name is too long
@put_one.route('/account/<id>', methods=['PUT'])
def account_put(id):

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify({'message': 'Please enter a name'}), 400)

    account = db.session.query(Account).get(id)

    if not account:
        return make_response(jsonify(
            {'message': 'Account ID doesn\'t exists'}), 400)

    account.name = data['name']
    db.session.commit()
    db.session.refresh(account)

    return make_response(jsonify(
        {'message': 'Account modified', 'account': account}), 200)


# FIXME : return an error if name is too long
@put_one.route('/mall/<id>', methods=['PUT'])
def mall_put(id):

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify({'message': 'Please enter a name'}), 400)

    mall = db.session.query(Mall).get(id)

    if not mall:
        return make_response(jsonify(
            {'message': 'Mall ID doesn\'t exists'}), 400)

    mall.name = data['name']
    db.session.commit()
    db.session.refresh(mall)

    return make_response(jsonify(
        {'message': 'Mall modified', 'mall': mall}), 200)


# FIXME : return an error if name is too long
@put_one.route('/unit/<id>', methods=['PUT'])
def unit_put(id):

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify(
            {'message': 'Please enter a name'}), 400)

    unit = db.session.query(Unit).get(id)

    if not unit:
        return make_response(jsonify(
            {'message': 'Unit ID doesn\'t exists'}), 400)

    unit.name = data['name']
    db.session.commit()
    db.session.refresh(unit)

    return make_response(jsonify(
        {'message': 'Unit modified', 'unit': unit}), 200)
