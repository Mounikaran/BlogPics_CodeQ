from django.db import models
import string as str
from random import choice
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


def generate_slug():
    n = 10
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits
    return ''.join(choice(random) for _ in range(n))

class Question(models.Model):
    question_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=300, unique=True)
    code = models.TextField(max_length=2000, null=True)
    slug = models.SlugField(unique=True, default=generate_slug, max_length=8)
    question_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Questions'
        ordering = ['-question_time']


class Answer(models.Model):
    question = models.ForeignKey('codeq.Question', related_name='answers', on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000)
    slug = models.SlugField(unique=True, max_length=8,default=generate_slug)
    answered_user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    answer_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('codeq:question_list')

class Reply(models.Model):
    answer = models.ForeignKey('codeq.Answer', related_name='reply', on_delete=models.CASCADE)
    reply_user = models.ForeignKey(User, related_name='reply', on_delete=models.CASCADE)
    reply = models.CharField(max_length=100)
    reply_time = models.DateTimeField(auto_now_add=True)
