from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно', widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Введите почту'}))
    username = forms.CharField(help_text='Это поле обязательно', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите логин'}
    ))
    password1 = forms.CharField(help_text='Это поле обязательно', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control-pwd',
            'placeholder': 'Введите пароль',
        }
    ))
    password2 = forms.CharField(help_text='Это поле обязательно',widget=forms.PasswordInput(
        attrs={
            'class': 'form-control-pwd',
            'placeholder': 'Введите пароль',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }
    ))
