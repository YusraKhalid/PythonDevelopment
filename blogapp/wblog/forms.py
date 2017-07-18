from django.forms import ModelForm, TextInput, PasswordInput, CharField, DateInput
from django.contrib.auth.forms import AuthenticationForm
from .models import UserInfo


class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30,
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = CharField(label="Password", max_length=30,
                         widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SignUpForm(ModelForm):
    username = CharField(label="Username", max_length=30, error_messages={'error': 'Invalid Username'},
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = CharField(label="Password", max_length=30,
                         widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = UserInfo
        fields = ['phone_no', 'address', 'date_of_birth', 'gender']
        widgets = {
            "phone_no": TextInput(attrs={'placeholder': 'Phone Number', 'name': 'phone_no', 'class': 'form-control'}),
            "address": TextInput(attrs={'placeholder': 'Address', 'name': 'address', 'class': 'form-control'}),
            "date_of_birth": DateInput({'placeholder': 'Date of Birth', 'name': 'dob', 'class': 'form-control'}),
            "gender": TextInput(attrs={'placeholder': 'Gender', 'name': 'gender', 'class': 'form-control'}),
        }
