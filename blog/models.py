from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_comments_xtd.moderation import moderator, XtdCommentModerator
from django_comments.moderation import CommentModerator
from django_comments_xtd.moderation import moderator
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid



class CustomProfile(models.Model):

    grades = (
        ('Aday', 'Aday'),
        ('Çırak', 'Çırak'),
        ('Kalfa', 'Kalfa'),
        ('Usta', 'Usta'),
        ('Büyük Usta', 'Büyük Usta'),
    )


    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_index=True)
    location = models.CharField(max_length=30, blank=True)
    job = models.CharField(max_length=255, blank=True)
    uni = models.CharField(max_length=255, blank=True)
    talents = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    rank = models.IntegerField(default=0)
    grade = models.CharField(max_length=25, choices=grades, default='Aday')
    avatar = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)








class QA(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    fixed = models.BooleanField('fixed', default=False)
    id = models.AutoField(primary_key=True)
    edit_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class QAnswer(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    edit_time = models.DateTimeField(null=True, blank=True)
    compare_id = models.CharField(max_length=250)
    unique = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.body







class AuthorApply(models.Model):
    name= models.CharField(max_length=255,  blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    job_talents= models.CharField(max_length=255, blank=True, null=True)
    uni = models.CharField(max_length=255, blank=True, null=True)
    rustudent =  models.CharField(max_length=255, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    apply_date = models.DateTimeField(default=timezone.now)
    approve= models.BooleanField('approve', default=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)






category= (
    ('Futbol', 'Futbol'),
    ('Finans', 'Finans'),
    ('Teknoloji', 'Teknoloji'),
)


class Document(models.Model):
    category = models.CharField(max_length=255, choices=category, blank=True, null=True)
    document = models.FileField(upload_to='documents/')
    file_name= models.CharField(max_length=255,  blank=True, null=True)
    dataset_title= models.CharField(max_length=255,  blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_5_row = models.CharField(max_length=2000,  blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, default="Veriseti")



class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager, self).get_queryset()\
                                         .filter(publish__lte=timezone.now())


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=255, choices=category, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    objects = PublicManager()  # Our custom manager.
    type = models.CharField(max_length=255, default="Blog")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       kwargs={'year': self.publish.year,
                               'month': self.publish.strftime('%b'),
                               'day': self.publish.strftime('%d'),
                               'slug': self.slug})







class PostCommentModerator(XtdCommentModerator):
    removal_suggestion_notification = False
    email_notification = False
    auto_moderate_field = 'publish'
    moderate_after = 365


moderator.register(Post, PostCommentModerator)
