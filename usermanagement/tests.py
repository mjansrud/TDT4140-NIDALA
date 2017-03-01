from django.test import TestCase

from usermanagement.models import *


class UserTokenTestCase(TestCase):
    def setUp(self):
        # Creates a user that is not yet activated
        self.user = User.objects.create(username='test')
        self.user.is_active = False
        self.user.save()

        # Cretes three different UserToken objects used in other tests
        self.expired_token = UserToken.objects.create(user=self.user)
        expired_date = timezone.now() - timedelta(hours=VALID_TIME + 1)
        self.expired_token.created = expired_date
        self.expired_token.save()

        self.activation_token = UserToken.objects.create(user=self.user)
        self.set_password_token = UserToken.objects.create(user=self.user)

    def test_expiration_of_expired_token(self):
        self.assertTrue(self.expired_token.expired(), 'Checks if UserToken expires')

    def test_activation_of_user(self):
        self.assertFalse(self.user.is_active, 'Checks if user is active before activation')
        self.activation_token.activate()
        self.assertTrue(self.user.is_active, 'Checks if user is active after activation')

        # Checks if the UserToken does exist after activation
        with self.assertRaises(UserToken.DoesNotExist):
            UserToken.objects.get(key=self.activation_token.key)

    def test_setting_password_with_token(self):
        password = 'test_password'
        self.assertFalse(self.user.check_password(password), 'Checks if password matches before its been set')
        self.set_password_token.set_password(password)
        self.assertTrue(self.user.check_password(password), 'Checks if password matches after its been set')

        # Checks if the UserToken does exist after activation
        with self.assertRaises(UserToken.DoesNotExist):
            UserToken.objects.get(key=self.set_password_token.key)

    def test_prune_expired_tokens(self):
        # Check is UserToken exists before deletion
        self.assertEqual(self.expired_token, UserToken.objects.get(key=self.expired_token.key))

        # Deletes all the expired tokens
        UserToken.objects.prune_expired()

        # Checks that the expired UserToken does not exist after deletion
        with self.assertRaises(UserToken.DoesNotExist):
            UserToken.objects.get(key=self.expired_token.key)
