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


# FIXME : return an error if name is too long
@app.route('/account', methods = ['POST'])
def account_post():

    data = request.get_json()

    if not data.get('name'):
        return make_response(jsonify({'message': 'Please enter a name'}), 400)

    account = Account(name=data['name'])   
    db.session.add(account)
    db.session.commit()
    db.session.refresh(account)

    return make_response(jsonify({'message': 'Account created', 'account': account}), 200)


# FIXME : return an error if name is too long
@app.route('/mall', methods = ['POST'])
def mall_post():

    data = request.get_json()

    if not data.get('name') or not data.get('account_id'):
        return make_response(jsonify({'message': 'Please enter a name and an account ID'}), 400)

    if not db.session.query(Account).get(data['account_id']):
        return make_response(jsonify({'message': 'Account ID doesn\'t exists'}), 400)

    mall = Mall(name=data['name'], account_id=data['account_id'])   
    db.session.add(mall)
    db.session.commit()
    db.session.refresh(mall)

    return make_response(jsonify({'message': 'Mall created', 'mall': mall}), 200)


# FIXME : return an error if name is too long
@app.route('/unit', methods = ['POST'])
def unit_post():

    data = request.get_json()

    if not data.get('name') or not data.get('mall_id'):
        return make_response(jsonify({'message': 'Please enter a name and an mall ID'}), 400)

    if not db.session.query(Mall).get(data['mall_id']):
        return make_response(jsonify({'message': 'Mall ID doesn\'t exists'}), 400)

    unit = Unit(name=data['name'], mall_id=data['mall_id'])   
    db.session.add(unit)
    db.session.commit()
    db.session.refresh(unit)

    return make_response(jsonify({'message': 'Unit created', 'unit': unit}), 200)