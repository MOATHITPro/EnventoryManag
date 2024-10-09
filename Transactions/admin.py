from django.contrib import admin
# Register your models here.

from .models import Receiving,Dispatch,ReceivingReturn,DispatchReturn,DamageOperation

admin.site.register(Receiving)
admin.site.register(Dispatch)
admin.site.register(ReceivingReturn)
admin.site.register(DispatchReturn)
admin.site.register(DamageOperation)

