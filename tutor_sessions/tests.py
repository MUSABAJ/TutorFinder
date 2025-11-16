from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from .models import BaseSession, BookedSession


class TutorSessionsSimpleTests(TestCase):
	def setUp(self):
		User = get_user_model()
		# create a student and a tutor (User model requires first_name/last_name)
		self.student = User.objects.create_user(username='student1', password='s', first_name='Stu', last_name='Dent', role='student')
		self.tutor = User.objects.create_user(username='tutor1', password='t', first_name='Tu', last_name='Tor', role='tutor')

	def test_create_base_and_booked_session(self):
		bs = BaseSession.objects.create(
			student=self.student,
			tutor=self.tutor,
			subject_name='Math',
			price=Decimal('100.00'),
			total_hours=Decimal('5.00'),
			remaining_hours=Decimal('5.00'),
			remaining_sessions=5
		)

		# __str__ includes tutor and student usernames
		self.assertIn('tutor1', str(bs))
		self.assertIn('student1', str(bs))

		booked = BookedSession.objects.create(
			base_session=bs,
			start_time='10:00',
			end_time='11:00',
			session_type='online'
		)

		self.assertEqual(booked.base_session, bs)

	def test_start_and_end_session_updates_remaining_hours(self):
		bs = BaseSession.objects.create(
			student=self.student,
			tutor=self.tutor,
			subject_name='Physics',
			price=Decimal('50.00'),
			total_hours=Decimal('2.00'),
			remaining_hours=Decimal('2.00'),
			remaining_sessions=2
		)

		# simulate a session that started 1 hour ago
		bs.current_start_time = timezone.now() - timedelta(hours=1)
		bs.save()

		# call end_session which should subtract ~1 hour from remaining_hours
		bs.end_session()

		# remaining_hours should be less than initial (allowing float rounding)
		self.assertLess(float(bs.remaining_hours), 2.0)
		# status should be either 'ongoing' or 'completed' depending on subtraction
		self.assertIn(bs.status, ('ongoing', 'completed'))
