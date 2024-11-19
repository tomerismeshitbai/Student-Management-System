from django.db import models
from students.models import Student
from courses.models import Course
import logging

logger = logging.getLogger('myapp')

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}: {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f'Attendance marked for {self.student.user.username} in course {self.course.name} on {self.date} as {self.status}')
        super().save(*args, **kwargs)
