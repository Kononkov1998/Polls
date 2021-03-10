from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from utils.constants import EMPTY_USER_AND_SESSION_KEY_ERROR


class Answer(models.Model):
    text = models.CharField(max_length=100, unique=True)


class Question(models.Model):
    TYPE_TEXT = 'text'
    TYPE_SINGLE = 'single'
    TYPE_MULTIPLE = 'multiple'

    TYPE_CHOICES = (
        (TYPE_TEXT, 'Ответ с текстом'),
        (TYPE_SINGLE, 'Ответ с выбором одного варианта'),
        (TYPE_MULTIPLE, 'Ответ с выбором нескольких вариантов'),
    )

    text = models.CharField(max_length=300, unique=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    answers = models.ManyToManyField(Answer, related_name='questions')


class Poll(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    questions = models.ManyToManyField(Question, related_name='polls')
    users = models.ManyToManyField(User, related_name='polls', through='UserPoll')


class UserPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=50, blank=True)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('user') and not cleaned_data.get('session_key'):
            raise ValidationError({'user': EMPTY_USER_AND_SESSION_KEY_ERROR})


class UserAnswer(models.Model):
    user_poll = models.ForeignKey(UserPoll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
