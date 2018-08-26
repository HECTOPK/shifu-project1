from django import forms
from alfa.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'image', 'content']
		widgets = {
			'title': forms.widgets.TextInput(attrs={'class': ' rounded-0 container',}),
		}
		labels = {
			'title': 'Title:',
			'image': 'Preview image:',
			'content': '',
		}

class LoginForm(forms.Form):
	username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control rounded-0'}))
	password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'type': 'password'}))

class EmailForm(forms.Form):
	email = forms.CharField(label=("Input email:"), widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'type': 'email'}))

class RegForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		widgets = {
			'username': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0', 'required': True}),
			'password': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0', 'type': 'password'}),
			'email': forms.widgets.TextInput(attrs={'class': 'form-control rounded-0', 'type': 'email'}),
		}
