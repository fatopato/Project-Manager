from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class ExcelForm(forms.Form):
    file = forms.FileField(label="Excel Dosyası")


class UserProfileForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'group']
        labels = {
            "username": "Kullanıcı adı",
            "first_name": "İsim",
            "last_name": "Soyisim",
            "email": "Email",
            "group": "Görev",
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        labels = {
            "username": "Kullanıcı adı",
            "first_name": "İsim",
            "last_name": "Soyisim",
            "email": "Email",
            "password1": "Şifre",
            "password2": "Şifre Onayı"
        }
        help_texts = {
            'username': "Zorunlu alan",
            'password2': "Şifrenizi tekrar girin",
        }
