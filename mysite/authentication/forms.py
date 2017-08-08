from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    def clean(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('password', 'passwrod does not match')
            self.add_error('confirm_password', 'password does not match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
