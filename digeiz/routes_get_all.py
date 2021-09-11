from flask import Flask, Blueprint, jsonify
from digeiz.models import Account, Mall, Unit


get_all = Blueprint('get_all', __name__)


@get_all.route('/accounts', methods = ['GET'])
def accounts_get():
    accounts = Account.query.all()

    return jsonify(accounts)


@get_all.route('/malls', methods = ['GET'])
def malls_get():
    malls = Mall.query.all()

    return jsonify(malls)


# FIXME : this may return the account id for each unit
@get_all.route('/units', methods = ['GET'])
def units_get():
    units = Unit.query.all()

    return jsonify(units)
