from flask import Flask, request, jsonify, make_response
from digeiz.models import Account, Mall, Unit
from digeiz import app, db


@app.route('/accounts', methods = ['GET'])
def accounts_get():
    accounts = Account.query.all()

    return jsonify(accounts)


@app.route('/malls', methods = ['GET'])
def malls_get():
    malls = Mall.query.all()

    return jsonify(malls)


# FIXME : this may return the account id for each unit
@app.route('/units', methods = ['GET'])
def units_get():
    units = Unit.query.all()

    return jsonify(units)


# FIXME : return the account created in response
# FIXME : return an error if name is too long
@app.route('/account', methods = ['POST'])
def account_post():

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify({'message': 'Please enter a name'}), 400)

    account = Account(name=data.get('name'))   
    db.session.add(account)
    db.session.commit()

    return make_response(jsonify({'message': 'Account created'}), 200)


# FIXME : return the mall created in response
# FIXME : return an error if name is too long
# FIXME : return an error if accound_id does not match an account
@app.route('/mall', methods = ['POST'])
def mall_post():

    data = request.get_json()

    if not data.get('name') or not data.get('account_id'):
        return make_response(jsonify({'message': 'Please enter a name and an account ID'}), 400)

    mall = Mall(name=data.get('name'), account_id=data.get('account_id'))   
    db.session.add(mall)
    db.session.commit()

    return make_response(jsonify({'message': 'Mall created'}), 200)


# FIXME : return the unit created in response
# FIXME : return an error if name is too long
# FIXME : return an error if mall_id does not match a mall
@app.route('/unit', methods = ['POST'])
def unit_post():

    data = request.get_json()

    if not data.get('name') or not data.get('mall_id'):
        return make_response(jsonify({'message': 'Please enter a name and an mall ID'}), 400)

    unit = Unit(name=data.get('name'), mall_id=data.get('mall_id'))   
    db.session.add(unit)
    db.session.commit()

    return make_response(jsonify({'message': 'Unit created'}), 200)