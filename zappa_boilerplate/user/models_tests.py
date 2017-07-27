# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError

import zappa_boilerplate.user.models as models
from zappa_boilerplate.test_utils import BaseTestCase


class TestUser(BaseTestCase):

    def test_user_create(self):

        user1 = models.User.create(self.session, username='foo1', email='foo1@bar.com', password='foobar1')
        user2 = models.User.create(self.session, username='foo2', email='foo2@bar.com', password='foobar2')
        self.session.commit()

        users = self.session.query(models.User).all()
        self.assertEqual(users, [user1, user2])

        # check that an IntegrityError gets raise if we try to create a user with the same username
        self.assertRaises(IntegrityError, models.User.create,
                          session=self.session, username='foo1', email='differentemail@bar.com', password='foofoo')
        self.session.rollback()

        # check that an IntegrityError gets raise if we try to create a user with the same email
        self.assertRaises(IntegrityError, models.User.create,
                          session=self.session, username='differentusername', email='foo1@bar.com', password='foofoo')

    def test_get_by_id(self):
        user1 = models.User.create(self.session, username='foo1', email='foo1@bar.com', password='foobar1')
        user2 = models.User.create(self.session, username='foo2', email='foo2@bar.com', password='foobar2')
        self.session.commit()

        self.assertEqual(models.User.get_by_id(self.session, user1.id), user1)
        self.assertEqual(models.User.get_by_id(self.session, user2.id), user2)
        self.assertIsNone(models.User.get_by_id(self.session, "not_a_user_id"))

    def test_repr(self):
        user = models.User.create(self.session, username='foo', email='foo@bar.com', password='foobar')
        self.assertEqual(repr(user), "<User('foo')>")

    def test_check_password(self):
        pwd = 'foobar'
        user = models.User.create(self.session, username='foo', email='foo@bar.com', password=pwd)
        self.assertTrue(user.check_password(pwd))
        self.assertFalse(user.check_password('not_the_password'))
