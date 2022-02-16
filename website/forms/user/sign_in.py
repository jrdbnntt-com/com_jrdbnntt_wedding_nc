from django import forms
from .. import StandardForm, widgets


class UsernamePasswordForm(StandardForm):
    username = forms.CharField(label='Username', max_length=150, required=True, widget=widgets.TextInput)
    password = forms.CharField(label='Password', max_length=150, required=True, widget=widgets.PasswordInput())

