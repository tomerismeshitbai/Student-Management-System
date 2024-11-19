from celery import Celery
from celery.task import periodic_task
from django.utils.timezone import now
from django.core.mail import send_mail

@periodic_task(run_every=timedelta(days=1))
def send_daily_report():
    students = Student.objects.all()
    report = "Daily Attendance and Grade Summary\n"
    
    for student in students:
        attendance_count = student.attendance_set.count()
        grade = Grade.objects.filter(student=student).last()
        report += f"{student.user.username}: Attendance: {attendance_count}, Last Grade: {grade.value if grade else 'N/A'}\n"
    
    send_mail(
        'Daily Report: Attendance and Grades',
        report,
        'from@example.com',
        ['admin@example.com'],
        fail_silently=False,
    )

@periodic_task(run_every=timedelta(weeks=1))
def send_weekly_performance_update():
    students = Student.objects.all()
    for student in students:
        report = f"Weekly Performance Report for {student.user.username}\n"

        attendance_count = student.attendance_set.count()
        grade = Grade.objects.filter(student=student).last()
        
        report += f"Attendance: {attendance_count}\n"
        report += f"Last Grade: {grade.value if grade else 'N/A'}\n"
        
        send_mail(
            'Weekly Performance Summary',
            report,
            'from@example.com',
            [student.user.email],
            fail_silently=False,
        )
