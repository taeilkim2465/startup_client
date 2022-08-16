from tkinter import CASCADE
from django.db import models
from django.utils import timezone
import datetime


positionchoice = (
    ('front-end', 'front-end'),
    ('back-end', 'back-end'),
    ('app', 'app'),
)

techstackchoice = (
    ('python', 'python'),
    ('django', 'django'),
    ('react', 'react'),
)

is_recruiting = (
    ('ing', '채용중'),
    ('end', '채용마감'),
)

class Post(models.Model):
    startup_name = models.CharField(max_length=20)
    thumbnail_image = models.ImageField(upload_to = "images/", null=True, blank=True)
    short_introduce = models.CharField(max_length = 200, null=True)
    short_form_video = models.CharField(max_length = 200, null=True)
    startup_introduce = models.TextField(null=True)
    startup_culture = models.TextField(null=True)
    startup_welfare = models.TextField(null=True)
    recruit_conference_video = models.CharField(max_length = 200, null=True)
    create_date = models.DateTimeField(timezone.now)
    def __str__(self):
        return str(self.startup_name)

class Recruit(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_recruiting = models.CharField(max_length = 200, choices=is_recruiting)
    recruit_ending = models.DateTimeField(default=timezone.now)
    recruit_position = models.CharField(max_length = 200, choices=positionchoice)
    techstack = models.CharField(max_length = 200, choices=techstackchoice)
    career = models.TextField(null=True)
    job_info = models.TextField(null=True)
    qualification = models.TextField(null=True)
    preference = models.TextField(null=True)
    def __str__(self):
        return str(self.id)+str(self.post_id)

class Image(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "images/", null=True, blank=True)
    def __str__(self):
        return str(self.id)+str(self.post_id)

class Tag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)
    def __str__(self):
        return str(self.tag)

class Employee(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    introduce = models.TextField(null=True)
    def __str__(self):
        return str(self.name)