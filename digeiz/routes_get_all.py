from flask import Flask, Blueprint, jsonify, make_response
from digeiz.models import Account, Mall, Unit


get_all = Blueprint('get_all', __name__)


@get_all.route('/accounts', methods = ['GET'])
def accounts_get():
    accounts = Account.query.all()

    return make_response(jsonify({'accounts': accounts}), 200)


@get_all.route('/malls', methods = ['GET'])
def malls_get():
    malls = Mall.query.all()

    return make_response(jsonify({'malls': malls}), 200)


@get_all.route('/units', methods = ['GET'])
def units_get():
    units = Unit.query.all()

    return make_response(jsonify({'units': units}), 200)
