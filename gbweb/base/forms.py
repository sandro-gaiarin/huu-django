from django.forms import ModelForm
from django import forms
from .models import CodeRoom



class CodeRoomForm(ModelForm):
    class Meta:
        model = CodeRoom
        fields = '__all__'

