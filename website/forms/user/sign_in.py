from django import forms

from website.forms import StandardForm, widgets


class UsernamePasswordForm(StandardForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(label='Username', max_length=150, required=True, widget=widgets.TextInput())
    password = forms.CharField(label='Password', max_length=150, required=True, widget=widgets.PasswordInput())

    def clear_sensitive_form_data(self):
        if 'password' in self.cleaned_data:
            del self.cleaned_data['password']
        if 'recaptcha_token' in self.cleaned_data:
            del self.cleaned_data['recaptcha_token']


class ReservationCodeForm(StandardForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput())
    reservation_code = forms.CharField(label="Reservation Code", max_length=10, required=True,
                                       widget=widgets.TextInput())

    def clear_sensitive_form_data(self):
        if 'reservation_code' in self.cleaned_data:
            del self.cleaned_data['reservation_code']
        if 'recaptcha_token' in self.cleaned_data:
            del self.cleaned_data['recaptcha_token']
