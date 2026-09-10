from django import forms
from .models import Productdetails
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']
       


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Productdetails
        fields = ['image', 'product_name', 'price', 'quantity', 'description']
