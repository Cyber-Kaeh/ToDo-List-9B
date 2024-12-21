from django import forms
from django.forms import ModelForm
from .models import ToDoItem


class TaskForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ('text', 'due_date')
        widgets = {
            "due_date": forms.DateInput(attrs={'type': 'date'}),
        }
