from django.forms import Form, ModelForm
from django import forms
from .models import ContactModel, Comment


class ContactForm(ModelForm):
    class Meta:
        model = ContactModel
        # fields = ['name', 'email', 'phone', 'message']
        fields = '__all__'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']