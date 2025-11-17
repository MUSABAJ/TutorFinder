from django.core.management.base import BaseCommand
from django.utils.timezone import now
from tutor_sessions.models import BookedSession
from notifications.models import  Notification
from notifications.utils import create_notification
from datetime import timedelta

class Command(BaseCommand):
    help = 'send sessoin reminder to students'

    def handle(self, *args, **kwargs):
        now_time = now()
        reminder_window = now_time + timedelta(hours=24)
        # Next Day reminder
        upcoming_sessions = BookedSession.objects.filter(
                                        start_time__gte=now_time,
                                        start_time__lte=reminder_window,
                                        notification_status = '0'
                                        )
        self.stdout.write(f"[*]>> Found --{upcoming_sessions.count()}-- sessions to notify")

        for session in upcoming_sessions:
            
            create_notification(recipient=session.tutor, user="TutorHUB",type='upcoming_session')
            create_notification(recipient=session.student, user="TutorHUB",type='upcoming_session')
            session.notification_status = '1'
            session.save()
        self.stdout.write(f"[*]>> succesfuly sent sessions reminders")
        
        # reminder an hour before
        reminder_window = now_time + timedelta(hours=1)
        today_sessions = BookedSession.objects.filter(
                                    start_time__gte=now_time,
                                    start_time__lte=reminder_window,
                                    notification_status = '1'
                                )
        for session in today_sessions:
            create_notification(recipient=session.tutor, user="TutorHUB",type='one_hr_session_reminder')
            create_notification(recipient=session.student, user="TutorHUB",type='one_hr_session_reminder')
            notification_status = '2'
            session.save()


        # reminder 5 minutes before
        reminder_window = now_time + timedelta(minutes=7)
        upcoming_sessions = BookedSession.objects.filter(
                                        start_time__gte=now_time,
                                        start_time__lte=reminder_window,
                                        notification_status = '2'

                                       )
        for session in upcoming_sessions:
            create_notification(recipient=session.tutor, user="TutorHUB",type='five_min_session_reminder')  
            create_notification(recipient=session.student, user="TutorHUB",type='five_min_session_reminder')
            session.notification_status = '3'
            session.save()
        
print(444444444444444444444444444444444444444444444444)        
print(444444444444444444444444444444444444444444444444)        
print(444444444444444444444444444444444444444444444444)        
print(444444444444444444444444444444444444444444444444)        
'''
    the Abouve to work
    create windows basic schedule task


'''
