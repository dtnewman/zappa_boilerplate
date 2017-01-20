from sqlalchemy.exc import IntegrityError, InvalidRequestError

import models
from template_project.test_utils import BaseTestCase


class TestAppointmentType(BaseTestCase):

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