from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from stack.models import Questions,UserProfile


class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

        

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())

class QuestionForm(ModelForm):
    
    class Meta:
        model=Questions
        fields=["description","image"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["bio","profile_pic"]
        

