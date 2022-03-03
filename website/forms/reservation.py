from . import StandardForm
from django import forms
from django.core.exceptions import ValidationError


class ActivateForm(StandardForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(label="Contact Email", required=True)
    email_verify = forms.EmailField(label="Verify Contact Email", required=True)

    def clear_sensitive_form_data(self):
        if 'recaptcha_token' in self.cleaned_data:
            del self.cleaned_data['recaptcha_token']

    def clean_email_verify(self):
        email = self.cleaned_data['email']
        email_verify = self.cleaned_data['email_verify']
        if email != email_verify:
            raise ValidationError("Email does not match")
