from django import forms
from .models import *


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
