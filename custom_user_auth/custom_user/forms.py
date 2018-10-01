"""
this module contains the forms of our app
"""
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser
from . import strings


class UserRegisterForm(forms.ModelForm):
    """
    this is a form class for user registration form
    """
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': strings.PASSWORD_REQUIRED, })

    class Meta:
        """Meta class for UserRegisterForm"""
        model = MyUser
        fields = ['username', 'email', 'password']
        error_messages = {
            'username': {
                'required': strings.USERNAME_REQUIRED,
                'max_length': strings.USERNAME_MAX_LENGTH,
            },
        }


class UserLoginForm(forms.Form):
    """
        this is a form class for user login form
        """
    username = forms.CharField(required=True,
                               error_messages={'required': strings.USER_USERNAME_REQUIRED})
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': strings.USER_PASSWORD_REQUIRED})


class UserEditForm(forms.ModelForm):
    """
        this is a form class for user edit form
    """

    class Meta:
        """Meta class for UserEditForm"""
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'email']
        error_messages = {
            'username': {
                'required': strings.USERNAME_REQUIRED,
                'max_length': strings.USERNAME_MAX_LENGTH
            },
            'first_name': {
                'max_length': strings.FIRSTNAME_MAX_LENGTH
            },
            'last_name': {
                'max_length': strings.LASTNAME_MAX_LENGTH
            },
        }


class UserChangePasswordForm(forms.Form):
    """
        this is a form class for user password change form
    """

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': strings.PASSWORD_MISMATCH,
        'password_incorrect': strings.PASSWORD_INCORRECT,
    }
    old_password = forms.CharField(
        label="Old password",
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        error_messages={'required': strings.OLD_PASSWORD_REQUIRED}
    )
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput,
        error_messages={'required': strings.PASSWORD1_REQUIRED}
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        widget=forms.PasswordInput,
        error_messages={'required': strings.PASSWORD2_REQUIRED}
    )

    def clean_new_password2(self):
        """
        this method check that the two passords are entered and they match
        :return: password2
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def clean_old_password(self):
        """
        this method checks that the old password that user has entered it correct or not
        :return: valid old_password
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        """Meta class for UserCreationForm"""
        model = MyUser
        fields = ('username',)

    def clean_password2(self):
        """ Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """ Save the provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        """Meta class for UserChangeForm"""
        model = MyUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial["password"]
