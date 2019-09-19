from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from .validators import validate_file_extension
from time import time
import datetime

# Create your models here.

USER_TYPE_CHOICES = (
    (1, 'STUDENT'),
    (2, 'TEACHER'),
)


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    role = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username


class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=True, null=True, related_name='teacher')
    student = models.ForeignKey(User, on_delete=True, null=True, related_name='student')
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/', validators=[validate_file_extension],blank=True, null=True)
    created_on = models.DateTimeField(default=datetime.datetime.now, null=True)
    deadline = models.DateField()

    def __str__(self):
        return self.name



class Submission(models.Model):
    assignment_name = models.ForeignKey(Assignment, on_delete=True)
    to_teacher = models.ForeignKey(User, on_delete=True, null=True, related_name='to_teacher')
    from_student = models.ForeignKey(User, on_delete=True, null=True, related_name='from_student')
    document = models.FileField(upload_to='documents/', validators=[validate_file_extension],blank=True)
    submission_date = models.DateField(blank=True, null=True)



class Credit(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=True)
    teacher_to = models.ForeignKey(User, on_delete=True, null=True, related_name='teacher_to')
    student_from = models.ForeignKey(User, on_delete=True, null=True, related_name='student_from')
    stars = models.IntegerField(default=0, blank=True, null=True)
    comments = models.CharField(max_length=200,default="", blank=True, null=True)

    def __str__(self):
        return self.comments


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=True,null=True, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=True,null=True, related_name='reciever')
    text = models.CharField(max_length=500)
    sent_time = models.DateTimeField()

    class Meta:
        ordering = ('sent_time',)

    def save(self):
        self.sent_time = datetime.datetime.now()
        super(Message, self).save()