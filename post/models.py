from __future__ import unicode_literals

import string as str
from random import choice
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_id():
    n = 50
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits
    return ''.join(choice(random) for _ in range(n))

def generate_comment_id():
    N = 8
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits
    return ''.join(choice(random) for _ in range(N))

class Post(models.Model):
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='post_photos/', default='default_img.png')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=50, default=generate_id)
    post_user = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post:postdetail', kwargs={'slug':self.slug})

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'posts'
        ordering = ['-uploaded_at']

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=8, default=generate_comment_id)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post:postlist',)

    def __str__(self):
        return self.comment_user + " " + self.slug
