from django.contrib import admin

# Register your models here.

from .models import Folders,Files

admin.site.register(Folders)

admin.site.register(Files)