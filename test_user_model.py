"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_is_following(self):
        """Are followers tracked?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        u2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            following=[u]
        )
        
        u3 = User(
            email="test3@test3.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u2, u3])
        db.session.commit()

        self.assertEqual(u2.is_following(u), 1)
        self.assertNotEqual(u2.is_following(u3), 1)
    
    def test_is_followed_by(self):
        """Are followed by users tracked"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        u2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            followers=[u]
        )
        
        u3 = User(
            email="test3@test3.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u2, u3])
        db.session.commit()

   
        self.assertEqual(u2.is_followed_by(u), 1)
        self.assertNotEqual(u2.is_followed_by(u3), 1)

    def test_user_authentication(self):
        """Does user authentication work?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url='test.com',
            bio='test',
            location='test'
        )

        db.session.add(u)
        db.session.commit()

        user = User.authenticate('testuser',
                                 'HASHED_PASSWORD')

        user2 = User.authenticate('testusere',
                                 'HASHED_PASSWORD')

        user3 = User.authenticate('testuser',
                                 'HASHED_PASSWORDe')

        # User should have no messages & no followers
        self.assertEqual(u, user)
        self.assertNotEqual(u, user2)
        self.assertNotEqual(u, user3)