from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User
import logging

logger = logging.getLogger('myapp')

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}: {self.grade}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f'Grade set for {self.student.user.username} in course {self.course.name}: {self.grade}')
        else:
            logger.info(f'Grade updated for {self.student.user.username} in course {self.course.name}: {self.grade}')
        super().save(*args, **kwargs)
