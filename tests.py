import json
import unittest

from digeiz import app, db


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

    def test_initial_accounts(self):
        """
        It should return an empty list when there is no account
        """
        response = app.test_client().get('/accounts')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['accounts'] == []

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
        It should return increment the account id when an account is created
        """
        response = app.test_client().post('/account', data=json.dumps(
            {"name": "my_account"}), content_type='application/json')
        data = json.loads(response.data)

        assert response.status_code == 200
        assert data['account']['id'] == 2


if __name__ == '__main__':
    unittest.main()
