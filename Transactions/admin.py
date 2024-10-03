from django.contrib import admin
# Register your models here.

from .models import Receiving,Dispatch

admin.site.register(Receiving)
admin.site.register(Dispatch)
