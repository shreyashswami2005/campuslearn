from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Attendance, Course, Enrollment, Lesson, Result


SAMPLE_COURSES = [
    {
        'title': 'Introduction to Python',
        'category': 'Computer Science',
        'description': (
            'Learn Python fundamentals for college coursework: variables, control flow, '
            'functions, and simple data structures used in labs and assignments.'
        ),
        'lessons': [
            (
                'Getting started',
                'Install Python and run your first script.\n\n'
                'Open a terminal and type:\npython --version\n\n'
                'Then create a file hello.py with:\nprint("Hello, campus!")\n\n'
                'Run it with: python hello.py',
            ),
            (
                'Variables and types',
                'Python uses dynamic typing. Common types:\n\n'
                '- int: whole numbers\n- float: decimals\n- str: text\n- bool: True/False\n\n'
                'Example:\nname = "Ada"\nage = 20\ngpa = 3.8',
            ),
            (
                'Functions',
                'Define reusable blocks with def:\n\n'
                'def greet(name):\n    return f"Welcome, {name}"\n\n'
                'print(greet("student"))',
            ),
        ],
    },
    {
        'title': 'College Writing Essentials',
        'category': 'Humanities',
        'description': (
            'Build clear essays and lab reports: thesis statements, paragraph structure, '
            'citations, and revising for clarity.'
        ),
        'lessons': [
            (
                'Thesis and outline',
                'A strong thesis is specific and arguable.\n\n'
                'Weak: Social media is bad.\n'
                'Strong: Campus discussion forums improve peer learning when moderated weekly.\n\n'
                'Outline: intro → 3 evidence paragraphs → counterpoint → conclusion.',
            ),
            (
                'Paragraph structure',
                'Each body paragraph needs:\n\n'
                '1. Topic sentence\n2. Evidence or example\n3. Explanation\n4. Link to thesis\n\n'
                'Keep one main idea per paragraph.',
            ),
        ],
    },
    {
        'title': 'Basics of Microeconomics',
        'category': 'Economics',
        'description': (
            'Core ideas for first-year economics: scarcity, supply and demand, elasticity, '
            'and how markets allocate resources.'
        ),
        'lessons': [
            (
                'Scarcity and choice',
                'Economics studies how people choose under scarcity.\n\n'
                'Opportunity cost = the next-best alternative you give up.\n\n'
                'Example: Studying for an extra hour means less time for a part-time shift.',
            ),
            (
                'Supply and demand',
                'Demand slopes down: higher price → lower quantity demanded.\n'
                'Supply slopes up: higher price → higher quantity supplied.\n\n'
                'Equilibrium is where quantity demanded equals quantity supplied.',
            ),
            (
                'Elasticity',
                'Price elasticity of demand measures responsiveness to price changes.\n\n'
                'Elastic: luxuries, many substitutes.\n'
                'Inelastic: necessities, few substitutes.',
            ),
        ],
    },
]


class Command(BaseCommand):
    help = 'Load sample courses and lessons for CampusLearn demo'

    def handle(self, *args, **options):
        User = get_user_model()
        teacher, created = User.objects.get_or_create(
            username='teacher',
            defaults={
                'email': 'teacher@campuslearn.local',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('Created staff user: teacher / teacher123'))
        else:
            if not teacher.is_superuser:
                teacher.is_staff = True
                teacher.is_superuser = True
                teacher.save(update_fields=['is_staff', 'is_superuser'])
            self.stdout.write('Staff user "teacher" already exists')

        created_courses = 0
        for data in SAMPLE_COURSES:
            course, was_created = Course.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'category': data['category'],
                    'is_published': True,
                    'created_by': teacher,
                },
            )
            if was_created:
                created_courses += 1
                for index, (title, content) in enumerate(data['lessons'], start=1):
                    Lesson.objects.create(
                        course=course,
                        title=title,
                        content=content,
                        order=index,
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Seed complete. New courses created: {created_courses}')
        )

        student, student_created = User.objects.get_or_create(
            username='student',
            defaults={'email': 'student@campuslearn.local'},
        )
        if student_created:
            student.set_password('student123')
            student.first_name = 'Riya'
            student.last_name = 'Sharma'
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student: student / student123'))
        else:
            self.stdout.write('Student user "student" already exists')

        python = Course.objects.filter(title='Introduction to Python').first()
        writing = Course.objects.filter(title='College Writing Essentials').first()
        if not python:
            self.stdout.write(self.style.WARNING('Sample courses missing; skip result/attendance seed'))
            return

        for course in filter(None, [python, writing]):
            Enrollment.objects.get_or_create(student=student, course=course)

        sample_results = [
            (python, 'Quiz 1 — Basics', Result.EXAM_QUIZ, 18, 20, 'A', date.today() - timedelta(days=20)),
            (python, 'Assignment 1', Result.EXAM_ASSIGNMENT, 42, 50, 'B+', date.today() - timedelta(days=12)),
            (python, 'Midterm', Result.EXAM_MIDTERM, 74, 100, 'B', date.today() - timedelta(days=5)),
        ]
        if writing:
            sample_results.append(
                (
                    writing,
                    'Essay draft',
                    Result.EXAM_ASSIGNMENT,
                    35,
                    40,
                    'A-',
                    date.today() - timedelta(days=8),
                )
            )

        results_created = 0
        for course, title, exam_type, marks, max_marks, grade, exam_date in sample_results:
            _, was = Result.objects.get_or_create(
                student=student,
                course=course,
                title=title,
                defaults={
                    'exam_type': exam_type,
                    'marks_obtained': marks,
                    'max_marks': max_marks,
                    'grade': grade,
                    'exam_date': exam_date,
                },
            )
            results_created += int(was)

        attendance_created = 0
        statuses = [
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_LATE,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_ABSENT,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_PRESENT,
            Attendance.STATUS_EXCUSED,
        ]
        for offset, status in enumerate(statuses):
            day = date.today() - timedelta(days=offset + 1)
            course = python if offset % 2 == 0 else (writing or python)
            _, was = Attendance.objects.get_or_create(
                student=student,
                course=course,
                date=day,
                defaults={'status': status},
            )
            attendance_created += int(was)

        self.stdout.write(
            self.style.SUCCESS(
                f'Sample academics: {results_created} results, {attendance_created} attendance rows'
            )
        )
