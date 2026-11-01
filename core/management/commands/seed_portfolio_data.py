from datetime import date, datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from availablity.models import Availablity, TutorPackage
from chat.models import Chat, Message
from feedback.models import FeedBack
from notifications.models import Notification
from payments.models import Payment
from resources.models import Resource
from tutor_sessions.models import BaseSession, BookedSession, VirtualClass
from users.models import StudentProfile, TutorProfile


ADDIS_ABABA = ZoneInfo("Africa/Addis_Ababa")
DEMO_PASSWORD = "Password@!23"

TUTORS = [
    {
        "key": "hana",
        "first_name": "Hana",
        "last_name": "Mekonnen",
        "city": "Addis Ababa",
        "subjects": "Mathematics, Physics",
        "language": "Amharic, English",
        "qualification": "BSc Mathematics, Addis Ababa University (demo)",
        "experience": "6 years",
        "hourly_rate": 650,
        "rating": Decimal("4.90"),
        "bio": "Fictional portfolio tutor specializing in clear, step-by-step mathematics and physics lessons.",
        "packages": [
            {
                "name": "Algebra Foundations",
                "subject": "Mathematics",
                "description": "Four focused lessons covering equations, functions, and problem-solving.",
                "session_type": "online",
                "price": Decimal("2400.00"),
                "total_session": 4,
                "session_duration": 60,
                "session_perweek": 2,
            },
            {
                "name": "Physics Exam Prep",
                "subject": "Physics",
                "description": "A five-lesson review of mechanics, energy, and exam techniques.",
                "session_type": "both",
                "price": Decimal("3500.00"),
                "total_session": 5,
                "session_duration": 60,
                "session_perweek": 2,
            },
        ],
    },
    {
        "key": "dawit",
        "first_name": "Dawit",
        "last_name": "Bekele",
        "city": "Hawassa",
        "subjects": "English, IELTS",
        "language": "Amharic, English",
        "qualification": "BA English Language and Literature (demo)",
        "experience": "8 years",
        "hourly_rate": 700,
        "rating": Decimal("4.80"),
        "bio": "Fictional portfolio tutor helping learners build confident academic and conversational English.",
        "packages": [
            {
                "name": "Academic English",
                "subject": "English",
                "description": "Writing, grammar, reading comprehension, and academic vocabulary.",
                "session_type": "online",
                "price": Decimal("2800.00"),
                "total_session": 4,
                "session_duration": 60,
                "session_perweek": 2,
            },
            {
                "name": "IELTS Speaking Lab",
                "subject": "IELTS",
                "description": "Speaking practice with structured feedback and timed mock prompts.",
                "session_type": "both",
                "price": Decimal("4200.00"),
                "total_session": 6,
                "session_duration": 45,
                "session_perweek": 2,
            },
        ],
    },
    {
        "key": "selam",
        "first_name": "Selam",
        "last_name": "Tesfaye",
        "city": "Bahir Dar",
        "subjects": "Biology, Chemistry",
        "language": "Amharic, English",
        "qualification": "BSc Biology, Bahir Dar University (demo)",
        "experience": "5 years",
        "hourly_rate": 600,
        "rating": Decimal("4.70"),
        "bio": "Fictional portfolio tutor making biology and chemistry approachable through practical examples.",
        "packages": [
            {
                "name": "Biology Essentials",
                "subject": "Biology",
                "description": "Cell biology, genetics, and concise exam-ready revision.",
                "session_type": "online",
                "price": Decimal("2200.00"),
                "total_session": 4,
                "session_duration": 60,
                "session_perweek": 2,
            },
            {
                "name": "Chemistry Problem Solving",
                "subject": "Chemistry",
                "description": "Guided practice in equations, stoichiometry, and core concepts.",
                "session_type": "in-person",
                "price": Decimal("3000.00"),
                "total_session": 5,
                "session_duration": 60,
                "session_perweek": 2,
            },
        ],
    },
    {
        "key": "yonas",
        "first_name": "Yonas",
        "last_name": "Alemu",
        "city": "Addis Ababa",
        "subjects": "Python, Computer Science",
        "language": "Amharic, English",
        "qualification": "BSc Computer Science, Addis Ababa University (demo)",
        "experience": "7 years",
        "hourly_rate": 850,
        "rating": Decimal("4.95"),
        "bio": "Fictional portfolio tutor introducing programming through small, practical Python projects.",
        "packages": [
            {
                "name": "Python Starter Course",
                "subject": "Python",
                "description": "Variables, control flow, functions, and a beginner portfolio project.",
                "session_type": "online",
                "price": Decimal("4000.00"),
                "total_session": 5,
                "session_duration": 60,
                "session_perweek": 2,
            },
            {
                "name": "Computer Science Foundations",
                "subject": "Computer Science",
                "description": "Algorithms, data structures, and computational thinking.",
                "session_type": "both",
                "price": Decimal("4800.00"),
                "total_session": 6,
                "session_duration": 60,
                "session_perweek": 2,
            },
        ],
    },
]

STUDENTS = [
    {
        "key": "mahi",
        "first_name": "Mahi",
        "last_name": "Fikru",
        "city": "Addis Ababa",
        "grade_level": "college",
        "learning_goal": "exam",
        "field_of_study": "Computer engineering",
        "favorite": "Mathematics and Python",
        "bio": "Fictional portfolio student preparing for university exams.",
    },
    {
        "key": "sami",
        "first_name": "Sami",
        "last_name": "Kebede",
        "city": "Hawassa",
        "grade_level": "secondary",
        "learning_goal": "language",
        "field_of_study": "Secondary education",
        "favorite": "English and science",
        "bio": "Fictional portfolio student building confidence in English and science.",
    },
    {
        "key": "abel",
        "first_name": "Abel",
        "last_name": "Worku",
        "city": "Bahir Dar",
        "grade_level": "college",
        "learning_goal": "skill",
        "field_of_study": "Life sciences",
        "favorite": "Biology",
        "bio": "Fictional portfolio student strengthening core science skills.",
    },
    {
        "key": "liya",
        "first_name": "Liya",
        "last_name": "Girma",
        "city": "Addis Ababa",
        "grade_level": "secondary",
        "learning_goal": "homework",
        "field_of_study": "Secondary education",
        "favorite": "Physics and chemistry",
        "bio": "Fictional portfolio student looking for structured weekly study support.",
    },
]

ENROLLMENTS = [
    ("hana", "mahi", 0, "completed", 5),
    ("dawit", "sami", 0, "confirmed", None),
    ("selam", "abel", 0, "completed", 5),
    ("yonas", "liya", 0, "pending", None),
    ("hana", "abel", 1, "confirmed", None),
    ("dawit", "mahi", 1, "completed", 4),
    ("selam", "sami", 1, "pending", None),
    ("yonas", "mahi", 1, "confirmed", None),
]

RESOURCE_TITLES = {
    "hana": [
        ("Algebra: Linear Equations", "A demo study guide for solving and checking linear equations."),
        ("Physics: Motion and Forces", "A demo revision outline for motion graphs and Newton's laws."),
    ],
    "dawit": [
        ("Academic Writing Checklist", "A demo checklist for clear paragraphs, transitions, and editing."),
        ("IELTS Speaking Practice Plan", "A demo weekly plan for timed speaking practice."),
    ],
    "selam": [
        ("Cell Biology Review", "A demo revision guide covering cells, organelles, and transport."),
        ("Chemistry Equation Practice", "A demo worksheet outline for balancing chemical equations."),
    ],
    "yonas": [
        ("Python First Steps", "A demo guide to variables, loops, and functions."),
        ("Algorithms in Everyday Life", "A demo introduction to breaking problems into steps."),
    ],
}


class Command(BaseCommand):
    help = "Create repeatable, fictional portfolio demo data without deleting existing records."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        now_local = timezone.localtime(timezone.now(), ADDIS_ABABA)

        tutors = {}
        for data in TUTORS:
            user, _ = User.objects.get_or_create(
                username=f"portfolio_tutor_{data['key']}",
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": f"portfolio.tutor.{data['key']}@example.com",
                    "role": "tutor",
                    "bio": data["bio"],
                    "country": "Ethiopia",
                    "city": data["city"],
                    "is_active": True,
                },
            )
            self._ensure_demo_password(user)
            tutors[data["key"]] = user
            TutorProfile.objects.update_or_create(
                user=user,
                defaults={
                    "language": data["language"],
                    "qualification": data["qualification"],
                    "experience": data["experience"],
                    "teaching_prefrence": "both",
                    "subjects": data["subjects"],
                    "horuly_rate": data["hourly_rate"],
                    "rating": data["rating"],
                    "is_verified": True,
                    "available": True,
                },
            )

        students = {}
        for data in STUDENTS:
            user, _ = User.objects.get_or_create(
                username=f"portfolio_student_{data['key']}",
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": f"portfolio.student.{data['key']}@example.com",
                    "role": "student",
                    "bio": data["bio"],
                    "country": "Ethiopia",
                    "city": data["city"],
                    "is_active": True,
                },
            )
            self._ensure_demo_password(user)
            students[data["key"]] = user
            StudentProfile.objects.update_or_create(
                user=user,
                defaults={
                    "learning_goal": data["learning_goal"],
                    "grade_level": data["grade_level"],
                    "favorite": data["favorite"],
                    "field_of_study": data["field_of_study"],
                },
            )

        packages = {}
        for tutor_data in TUTORS:
            tutor = tutors[tutor_data["key"]]
            for package_data in tutor_data["packages"]:
                package, _ = TutorPackage.objects.update_or_create(
                    tutor=tutor,
                    name=package_data["name"],
                    defaults={
                        "description": package_data["description"],
                        "session_type": package_data["session_type"],
                        "is_active": True,
                        "price": package_data["price"],
                        "total_session": package_data["total_session"],
                        "session_duration": package_data["session_duration"],
                        "session_perweek": package_data["session_perweek"],
                    },
                )
                packages[(tutor_data["key"], package_data["subject"])] = package

        for index, tutor_data in enumerate(TUTORS):
            starts = []
            for day_offset in range(1, 8):
                start = self._local_datetime(
                    now_local.date() + timedelta(days=day_offset),
                    9 + ((index + day_offset) % 7),
                    0,
                )
                end = start + timedelta(minutes=60)
                starts.append(
                    {
                        "start": start.isoformat(),
                        "end": end.isoformat(),
                        "title": "Portfolio demo availability",
                    }
                )
            Availablity.objects.update_or_create(
                tutor=tutors[tutor_data["key"]],
                defaults={"availablity": starts},
            )

        created_bookings = {}
        for enrollment_index, (tutor_key, student_key, package_index, status, rating) in enumerate(ENROLLMENTS):
            tutor_data = next(item for item in TUTORS if item["key"] == tutor_key)
            tutor = tutors[tutor_key]
            package_data = tutor_data["packages"][package_index]
            package = packages[(tutor_key, package_data["subject"])]
            student = students[student_key]
            is_completed = status == "completed"
            is_confirmed = status == "confirmed"
            completed_count = 3 if is_completed else (1 if is_confirmed else 0)
            total_hours = Decimal(package.total_session * package.session_duration) / Decimal(60)
            remaining_sessions = max(package.total_session - completed_count, 0)
            remaining_hours = (
                Decimal(remaining_sessions * package.session_duration) / Decimal(60)
            )
            base_session, _ = BaseSession.objects.update_or_create(
                student=student,
                tutor=tutor,
                package=package,
                subject_name=package_data["subject"],
                defaults={
                    "total_session": package.total_session,
                    "price": package.price,
                    "is_payed": is_completed or is_confirmed,
                    "session_duration": package.session_duration,
                    "total_hours": total_hours,
                    "remaining_hours": remaining_hours,
                    "status": status,
                    "remaining_sessions": remaining_sessions,
                },
            )

            if is_completed:
                offsets = [-14, -8, -2]
                booking_statuses = ["completed", "completed", "completed"]
            elif is_confirmed:
                offsets = [-3, 2, 7]
                booking_statuses = ["completed", "scheduled", "up_comming"]
            else:
                offsets = [3, 10]
                booking_statuses = ["scheduled", "up_comming"]

            tutor_booking_ids = created_bookings.setdefault(tutor_key, [])
            for booking_index, (day_offset, booking_status) in enumerate(zip(offsets, booking_statuses), 1):
                start = self._local_datetime(
                    now_local.date() + timedelta(days=day_offset),
                    10 + (enrollment_index % 5),
                    0,
                )
                end = start + timedelta(minutes=package.session_duration)
                topic = f"{package_data['subject']} lesson {booking_index}"
                session_type = (
                    "offline" if package.session_type == "in-person" else "online"
                )
                room_name = (
                    f"portfolio-demo-{tutor_key}-{enrollment_index}-{booking_index}"
                    if session_type == "online"
                    else ""
                )
                booked, _ = BookedSession.objects.update_or_create(
                    base_session=base_session,
                    topic=topic,
                    defaults={
                        "status": booking_status,
                        "start_time": start.isoformat(),
                        "end_time": end.isoformat(),
                        "location": tutor_data["city"] if session_type == "offline" else "",
                        "room_name": room_name,
                        "session_type": session_type,
                        "notification_status": "0",
                    },
                )
                BookedSession.objects.filter(pk=booked.pk).update(schedule_date=start)
                if room_name:
                    VirtualClass.objects.update_or_create(
                        session=booked,
                        defaults={"room_name": room_name},
                    )
                tutor_booking_ids.append(booked.pk)

            payment_status = "success" if is_completed else ("held" if is_confirmed else "pending")
            Payment.objects.update_or_create(
                session=base_session,
                defaults={
                    "student": student,
                    "tutor": tutor,
                    "amount": package.price,
                    "status": payment_status,
                    "refrence_id": f"DEMO-PORTFOLIO-{enrollment_index + 1:03d}",
                },
            )

            if rating:
                FeedBack.objects.update_or_create(
                    session=base_session,
                    defaults={
                        "student": student,
                        "tutor": tutor,
                        "rating": rating,
                        "feedback": (
                            f"Portfolio demo review: {tutor.first_name} explained "
                            f"{package_data['subject'].lower()} clearly and gave useful practice."
                        ),
                    },
                )

            self._seed_chat(tutor, student, now_local)
            self._seed_notification(
                tutor,
                f"Portfolio demo: {student.first_name} has a {status} {package_data['subject']} lesson package.",
                "/sessions/",
            )
            self._seed_notification(
                student,
                f"Portfolio demo: your {package_data['subject']} package with {tutor.first_name} is {status}.",
                "/sessions/",
            )

        for tutor_key, resources in RESOURCE_TITLES.items():
            tutor = tutors[tutor_key]
            for title, description in resources:
                Resource.objects.update_or_create(
                    tutor=tutor,
                    title=title,
                    defaults={
                        "subject": title.split(":")[0] if ":" in title else title.split()[0],
                        "description": description,
                        "video_link": "",
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Portfolio demo data is ready: 4 fictional tutors, 4 fictional students, "
                "8 packages, 8 course enrollments, lesson schedules, payments, reviews, "
                "availability, resources, chats, and notifications. "
                "All seeded accounts use the shared demo password."
            )
        )

    @staticmethod
    def _local_datetime(day: date, hour: int, minute: int) -> datetime:
        return datetime.combine(day, time(hour, minute), tzinfo=ADDIS_ABABA)

    @staticmethod
    def _ensure_demo_password(user):
        if not user.check_password(DEMO_PASSWORD):
            user.set_password(DEMO_PASSWORD)
            user.save(update_fields=["password"])

    @staticmethod
    def _seed_chat(tutor, student, now_local):
        participant_ids = {tutor.pk, student.pk}
        chat = next(
            (
                candidate
                for candidate in Chat.objects.filter(participants=tutor).prefetch_related("participants")
                if {participant.pk for participant in candidate.participants.all()} == participant_ids
            ),
            None,
        )
        if chat is None:
            chat = Chat.objects.create()
            chat.participants.add(tutor, student)

        messages = [
            (student, tutor, "Hello! I would like to focus on the next course topic."),
            (tutor, student, "Welcome! I have added a practice plan for our next lesson."),
            (student, tutor, "Thank you. I will review the demo study material."),
            (tutor, student, "Great. Bring your questions and we will work through them together."),
        ]
        for index, (sender, receiver, content) in enumerate(messages):
            message, created = Message.objects.get_or_create(
                chat=chat,
                sender=sender,
                receiver=receiver,
                content=content,
                defaults={"is_read": index < 3},
            )
            if created:
                Message.objects.filter(pk=message.pk).update(
                    timestamp=now_local - timedelta(days=1, minutes=15 - index * 3)
                )

    @staticmethod
    def _seed_notification(recipient, message, link):
        Notification.objects.get_or_create(
            recipient=recipient,
            message=message,
            defaults={"link": link, "is_read": False},
        )
