from flask import Flask, Blueprint, jsonify, make_response
from digeiz.models import Account, Mall, Unit
from digeiz import db


get_one = Blueprint('get_one', __name__)


@get_one.route('/account/<id>', methods = ['GET'])
def account_get(id):
    account = db.session.query(Account).get(id)

    if not account:
        return make_response(jsonify({'message': 'Account ID doesn\'t exists'}), 400)

    return make_response(jsonify({'account': account}), 200)


@get_one.route('/mall/<id>', methods = ['GET'])
def mall_get(id):
    mall = db.session.query(Mall).get(id)

    if not mall:
        return make_response(jsonify({'message': 'Mall ID doesn\'t exists'}), 400)

    return make_response(jsonify({'mall': mall}), 200)


@get_one.route('/unit/<id>', methods = ['GET'])
def unit_get(id):
    unit = db.session.query(Unit).get(id)

    if not unit:
        return make_response(jsonify({'message': 'Unit ID doesn\'t exists'}), 400)

    return make_response(jsonify({'unit': unit}), 200)
