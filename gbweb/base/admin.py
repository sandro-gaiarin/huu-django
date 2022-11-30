from django.contrib import admin

# Register your models here.
from .models import CodeRoom, Topic, Message, User


admin.site.register(CodeRoom)
admin.site.register(Topic)
admin.site.register(Message)
