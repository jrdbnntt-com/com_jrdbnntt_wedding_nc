from django import forms
from .. import StandardForm, widgets


class UsernamePasswordForm(StandardForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(label='Username', max_length=150, required=True, widget=widgets.TextInput())
    password = forms.CharField(label='Password', max_length=150, required=True, widget=widgets.PasswordInput())

    def clear_sensitive_form_data(self):
        if 'password' in self.cleaned_data:
            del self.cleaned_data['password']
        if 'recaptcha_token' in self.cleaned_data:
            del self.cleaned_data['recaptcha_token']
