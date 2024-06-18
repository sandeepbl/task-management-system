import unittest
from app import app, db
from app.models import User


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_user(self):
        user = User(username='testuser7', first_name='Test', last_name='User', role='User', display_pic_url="display_pic_url")
        user.set_hashed_password('password123')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        with app.app_context():
            retrieved_user = db.session.query(User).filter_by(username='testuser7').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser7')
        with app.app_context():
            user_to_delete = db.session.query(User).filter_by(username='testuser7').first()
            db.session.delete(user_to_delete)
            db.session.commit()
    def test_check_password(self):
        user = User(username='testuser11', first_name='Test', last_name='User', role='User',display_pic_url='display_pic_url')
        user.set_hashed_password('password123')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        with app.app_context():
            retrieved_user = db.session.query(User).filter_by(username='testuser11').first()
        self.assertTrue(retrieved_user.check_password('password123'))
        with app.app_context():
            user_to_delete = db.session.query(User).filter_by(username='testuser11').first()
            db.session.delete(user_to_delete)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
