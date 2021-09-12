from flask import Blueprint, jsonify, make_response, request

from digeiz import db
from digeiz.models import Account, Mall, Unit

post_one = Blueprint('post_one', __name__)


# FIXME : return an error if name is too long
@post_one.route('/account', methods=['POST'])
def account_post():

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify({'message': 'Please enter a name'}), 400)

    account = Account(name=data['name'])
    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)

    return make_response(jsonify(
        {'message': 'Account created', 'account': account}), 200)


# FIXME : return an error if name is too long
@post_one.route('/mall', methods=['POST'])
def mall_post():

    data = request.get_json()

    if not data.get('name') or not data.get('account_id'):
        return make_response(jsonify(
            {'message': 'Please enter a name and an account ID'}), 400)

    if not db.session.query(Account).get(data['account_id']):
        return make_response(jsonify(
            {'message': 'Account ID doesn\'t exists'}), 400)

    mall = Mall(name=data['name'], account_id=data['account_id'])
    db.session.add(mall)
    db.session.commit()
    db.session.refresh(mall)

    return make_response(jsonify(
        {'message': 'Mall created', 'mall': mall}), 200)


# FIXME : return an error if name is too long
@post_one.route('/unit', methods=['POST'])
def unit_post():

    data = request.get_json()

    if not data.get('name') or not data.get('mall_id'):
        return make_response(jsonify(
            {'message': 'Please enter a name and a mall ID'}), 400)

    mall = db.session.query(Mall).get(data['mall_id'])
    if not mall:
        return make_response(jsonify(
            {'message': 'Mall ID doesn\'t exists'}), 400)

    account_id = mall.account_id
    unit = Unit(
        name=data['name'], mall_id=data['mall_id'], account_id=account_id)
    db.session.add(unit)
    db.session.commit()
    db.session.refresh(unit)

    return make_response(jsonify(
        {'message': 'Unit created', 'unit': unit}), 200)
