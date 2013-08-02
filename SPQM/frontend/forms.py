import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


def email_valid(email):
    regex = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    return re.match(regex, email)


class LoginUserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
        }),
        max_length=32,
    )

    password = forms.CharField(
        min_length=6,
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'autocomplete': 'off'
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('User with this information does not exist.'), code='username_not_valid')
        return username


class RegisterUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': _('Email')
        }),
        max_length=256
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'data-toggle': 'tooltip',
            'title': 'Username is optional',
            'class': 'start-tooltip optional-input'
        }),
        max_length=32,
        required=False
    )

    password = forms.CharField(
        min_length=6,
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'autocomplete': 'off'
        })
    )

    password2 = forms.CharField(
        min_length=6,
        max_length=32,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Repeat Password'),
            'autocomplete': 'off'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email is already taken.'), code='email_taken')
        elif not email_valid(email):
            raise forms.ValidationError(_('Email is not valid.'), code='email_not_valid')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_('Passwords do not match'), code='passwords_do_not_match')
        return password2


class ContactForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Your First Name',
            'class': 'span3'
        }),
        max_length=32
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Last Name',
            'class': 'span3'
        }),
        max_length=32
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your email address',
            'class': 'span3'
        }),
        max_length=256
    )

    subject = forms.ChoiceField(
        choices=[
            ('General Customer Service', 'General Customer Service'),
            ('Suggestions', 'Suggestions')
        ]
    )

    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'class': 'input-xlarge span6'
        }),
        max_length=2000
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email_valid(email):
            raise forms.ValidationError(_('Email is not valid.'), code='email_not_valid')
        return email


class AddPersonForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'span3'
        }),
        max_length=32
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'span3'
        }),
        max_length=32
    )

    fictional = forms.BooleanField()

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'placeholder': 'Description',
            'class': 'input-xlarge span6'
        }),
        max_length=2000
    )

    video = forms.CharField(
        label='Video',
        widget=forms.TextInput(attrs={
            'placeholder': 'Youtube or Vimeo url',
            'class': 'span6'
        }),
        max_length=200
    )

    quote = forms.CharField(
        label='Quote',
        widget=forms.Textarea(attrs={
            'placeholder': 'Copy-paste Quote here',
            'class': 'span6'
        }),
        max_length=200
    )

    quotes = forms.CharField(
        label='',
        max_length=10000,
        required=False,
        widget=forms.HiddenInput()
    )

    images = forms.CharField(
        label='',
        max_length=10000,
        required=False,
        widget=forms.HiddenInput()
    )

    videos = forms.CharField(
        label='',
        max_length=10000,
        required=False,
        widget=forms.HiddenInput()
    )

