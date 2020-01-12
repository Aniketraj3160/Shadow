from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# class Journalist_Form(ModelForm):

#     class Meta:
#         model = Journalist
#         fields = ['profile_complete']


# class Anonymous_Form(ModelForm):

#     class Meta:
#         model = Anonymous
#         fields = ['profile_complete']


# class Authority_Form(ModelForm):

#     class Meta:
#         model = Authority
#         fields = ['profile_complete']


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'bio']

class UserRegisterForm(UserCreationForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        help_texts = {
            'username' :None,
            'password' :None,
            
        }
        fields = ['username','password1','password2','captcha']

