from django.contrib import admin
from .models import GITCommits, GITComments

# Register your models here.
admin.site.register(GITCommits)
admin.site.register(GITComments)
