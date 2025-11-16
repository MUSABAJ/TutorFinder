from django.test import TestCase
from django.contrib.auth import get_user_model


class SimpleUserTests(TestCase):
	def setUp(self):
		self.User = get_user_model()

	def test_create_user_and_login(self):
		"""Create a user, verify role/defaults and that login works."""
		user = self.User.objects.create_user(
			username='testuser', password='password123', first_name='Test', last_name='User'
		)

		# default role should be 'student'
		self.assertEqual(user.role, 'student')
		self.assertTrue(user.is_student())
		self.assertFalse(user.is_tutor())

		# string representation
		self.assertEqual(str(user), 'testuser')

		# login via the test client
		logged_in = self.client.login(username='testuser', password='password123')
		self.assertTrue(logged_in)

	def test_create_tutor_role(self):
		"""Create a user with tutor role and check helper methods."""
		user = self.User.objects.create_user(
			username='tutor1', password='tpass', first_name='Tutor', last_name='One', role='tutor'
		)
		self.assertEqual(user.role, 'tutor')
		self.assertTrue(user.is_tutor())
		self.assertFalse(user.is_admin())

