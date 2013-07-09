import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegisterUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Email')})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'data-toggle': 'tooltip',
            'title': 'Username is optional',
            'class': 'start-tooltip'
        }),
        max_length=32,
        required=False
    )

    password = forms.CharField(
        min_length=6,
        max_length=32,
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'autocomplete': 'off'})
    )

    password2 = forms.CharField(
        min_length=6,
        max_length=32,
        widget=forms.PasswordInput(attrs={'placeholder': _('Repeat Password'), 'autocomplete': 'off'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        regex = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email is already taken.'), code='email_taken')
        elif not re.match(regex, email):
            raise forms.ValidationError(_('Email is not valid.'), code='email_not_valid')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(_('Passwords do not match'), code='passwords_do_not_match')
        return password2