import json
import unittest

from digeiz import app, db
from digeiz.models import Account, Mall, Unit


class PostOneTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Creates a new database for the unit test to use
        """
        cls.app = app
        db.init_app(cls.app)
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        db.drop_all()
        db.create_all()

    # ===========================================================
    # ACCOUNT
    # ===========================================================

    def test_initial_accounts(self):
        """
        It should return an empty list when there is no account
        """
        response = app.test_client().get('/accounts')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['accounts'] == []

    def test_post_account_error(self):
        """
        It should return an error when creating an account with no name
        """
        response = app.test_client().post('/account', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name'

    def test_post_accounts(self):
        """
        It should return the account id when an account is created
        It should return an empty mall list when an account is created
        """
        response = app.test_client().post('/account', data=json.dumps(
            {"name": "my_account"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['account']['id'] == 1
        assert data['account']['malls'] == []

    def test_post_accounts_again(self):
        """
        It should increment the account id when an account is created
        """

        db.session.add(Account(name='my_account'))
        db.session.commit()

        response = app.test_client().post('/account', data=json.dumps(
            {"name": "my_account"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['account']['id'] == 2

    def test_delete_account(self):
        """
        It should delete the account
        It should delete the nested malls
        It should delete the nested units
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().delete('/account/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['message'] == 'Account deleted'

        response = app.test_client().get('/accounts')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['accounts'][0]['id'] == 2

        response = app.test_client().get('/malls')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['malls'] == []

        response = app.test_client().get('/units')
        data = json.loads(response.data)

        print(data)

        assert response.status_code == 200
        assert data['units'] == []

    def test_delete_account_errors(self):
        """
        It should return an error if the account doesn't exists
        """

        response = app.test_client().delete('/account/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Account ID doesn\'t exists'

    def test_rename_account(self):
        """
        It should return an error if the account doesn't exists
        It should return an error if no name is provided
        It should rename the account if exists
        """

        response = app.test_client().put('/account/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Account ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.commit()

        response = app.test_client().put('/account/1', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name'

        response = app.test_client().put('/account/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['account']['name'] == 'toto'

    def test_get_one_account(self):
        """
        It should return an error if the account doesn't exists
        It should return the account if exists
        """

        response = app.test_client().get('/account/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Account ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.commit()

        response = app.test_client().get('/account/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['account']['id'] == 1

    # ===========================================================
    # MALL
    # ===========================================================

    def test_post_mall_error(self):
        """
        It should return an error when creating a mall with no account id
        It should return an error when creating a mall with an account id that
        doesn't exists
        """
        response = app.test_client().post('/mall', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name and an account ID'

        response = app.test_client().post(
            '/mall',
            data=json.dumps({"name": "my_mall", "account_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Account ID doesn\'t exists'

    def test_post_mall(self):
        """
        It should return the mall nested in the account list when a mall is
        created
        """

        db.session.add(Account(name='my_account'))
        db.session.commit()

        response = app.test_client().post(
            '/mall',
            data=json.dumps({"name": "my_mall", "account_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        response = app.test_client().get('/accounts')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['accounts'][0]['malls'][0]['id'] == 1
        assert data['accounts'][0]['malls'][0]['name'] == 'my_mall'

    def test_post_mall_again(self):
        """
        It should increment the mall id when an account is created
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall'))
        db.session.commit()

        response = app.test_client().post(
            '/mall',
            data=json.dumps({"name": "my_mall", "account_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        response = app.test_client().get('/malls')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['malls'][0]['id'] == 1
        assert data['malls'][1]['id'] == 2

    def test_delete_mall(self):
        """
        It should delete the mall
        It should delete the nested units
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().delete('/mall/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['message'] == 'Mall deleted'

        response = app.test_client().get('/malls')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['malls'][0]['id'] == 2

        response = app.test_client().get('/units')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['units'] == []

    def test_delete_mall_errors(self):
        """
        It should return an error if the mall doesn't exists
        """

        response = app.test_client().delete('/mall/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Mall ID doesn\'t exists'

    def test_rename_mall(self):
        """
        It should return an error if the mall doesn't exists
        It should return an error if no name is provided
        It should rename the mall if exists
        """

        response = app.test_client().put('/mall/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Mall ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.commit()

        response = app.test_client().put('/mall/1', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name'

        response = app.test_client().put('/mall/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['mall']['name'] == 'toto'

    def test_get_one_mall(self):
        """
        It should return an error if the mall doesn't exists
        It should return the mall if exists
        """

        response = app.test_client().get('/mall/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Mall ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.commit()

        response = app.test_client().get('/mall/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['mall']['id'] == 1

    # ===========================================================
    # UNIT
    # ===========================================================

    def test_post_unit_error(self):
        """
        It should return an error when creating a unit with no mall id
        It should return an error when creating a unit with an mall id that
        doesn't exists
        """
        response = app.test_client().post('/unit', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name and a mall ID'

        response = app.test_client().post(
            '/unit',
            data=json.dumps({"name": "my_unit", "mall_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Mall ID doesn\'t exists'

    def test_post_unit(self):
        """
        It should return the unit nested in the account list when a unit is
        created
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.commit()

        response = app.test_client().post(
            '/unit',
            data=json.dumps({"name": "my_unit", "mall_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        response = app.test_client().get('/accounts')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['accounts'][0]['malls'][0]['units'][0]['id'] == 1

    def test_post_unit_again(self):
        """
        It should increment the unit id when a unit is created
        It should return the accout id when a unit is created
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().post(
            '/unit',
            data=json.dumps({"name": "my_unit", "mall_id": 1}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        response = app.test_client().get('/units')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['units'][0]['id'] == 1
        assert data['units'][1]['id'] == 2
        assert data['units'][1]['account_id'] == 1

    def test_delete_unit(self):
        """
        It should delete the unit
        """

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().delete('/unit/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['message'] == 'Unit deleted'

        response = app.test_client().get('/units')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['units'][0]['id'] == 2

    def test_delete_unit_errors(self):
        """
        It should return an error if the unit doesn't exists
        """

        response = app.test_client().delete('/unit/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Unit ID doesn\'t exists'

    def test_rename_unit(self):
        """
        It should return an error if the unit doesn't exists
        It should return an error if no name is provided
        It should rename the unit if exists
        """

        response = app.test_client().put('/unit/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Unit ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().put('/unit/1', data=json.dumps(
            {}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Please enter a name'

        response = app.test_client().put('/unit/1', data=json.dumps(
            {"name": "toto"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['unit']['name'] == 'toto'

    def test_get_one_unit(self):
        """
        It should return an error if the unit doesn't exists
        It should return the unit if exists
        """

        response = app.test_client().get('/unit/1')
        data = json.loads(response.data)

        assert response.status_code == 400
        assert data['message'] == 'Unit ID doesn\'t exists'

        db.session.add(Account(name='my_account'))
        db.session.add(Mall(name='my_mall', account_id=1))
        db.session.add(Unit(name='my_unit', mall_id=1, account_id=1))
        db.session.commit()

        response = app.test_client().get('/unit/1')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['unit']['id'] == 1


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
