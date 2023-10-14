from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Predict

class signup(UserCreationForm):
    password2=forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        label={'email':"Email",'username':'Username','first_name':'First Name','last_name':'Last Name'}

class EditUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','date_joined','last_login','is_active']
        labels={'email':'Email'}


class PredictForm(forms.ModelForm):
    class Meta:
        model = Predict
        fields = ('prediction_image',)
        labels = {'prediction_image': 'Select Histopathology Image for Prediction'}
        

