from django.db import models
from users.models import User
from students.models import Student
import logging

logger = logging.getLogger('myapp')


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f'Student {self.student.user.username} enrolled in course {self.course.name}')
        super().save(*args, **kwargs)
