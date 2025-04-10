from django.db import models

import uuid

from django.contrib.auth.models import User

from django.utils.deconstruct import deconstructible
import os

# Create your models here.


class BaseClass(models.Model):

    uuid = models.SlugField(default=uuid.uuid4,unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class Folders(BaseClass):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    folder_locked = models.BooleanField(default=True)

    folder_nonce = models.BinaryField(null=True,blank=True)

    folder_password = models.BinaryField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.name}'
    

    class Meta :

        verbose_name = 'Folders'

        verbose_name_plural = 'Folders'



@deconstructible
class PathAndRename:
    def __init__(self, folder_name_attribute):
        self.folder_name_attribute = folder_name_attribute

    def __call__(self, instance, filename):
        # Access the folder name dynamically and build the path
        folder_name = getattr(instance, self.folder_name_attribute).name
        return os.path.join('uploads', folder_name, filename)        

class Files(BaseClass):

    folder = models.ForeignKey('Folders',related_name='files', on_delete=models.CASCADE)

    file = models.FileField(upload_to=PathAndRename('folder'))

    def __str__(self):

        return f'{self.folder.name} files'
    

    class Meta :

        verbose_name = 'Files'

        verbose_name_plural = 'Files'

class ReportActionChoices(models.TextChoices):

    UNLOCKED = 'Unlocked','Unlocked'

    LOCKED = 'Locked','Locked'

    VIEWED = 'Viewed','Viewed'

    ADDED = 'Added','Added'

    DOWNLOADED = 'Downloaded','Downloaded'

    DELETED = 'Deleted','Deleted'

class Reports(BaseClass):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    folder_name = models.CharField(max_length=100)

    action = models.CharField(max_length=20,choices=ReportActionChoices.choices)

    action_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.user.first_name} {self.user.last_name} Reports'
    

    class Meta :

        verbose_name = 'Reports'

        verbose_name_plural = 'Reports'