from django import forms
from django.core.exceptions import ValidationError

from website.forms import StandardForm
from website.forms import widgets


class ActivateForm(StandardForm):
    recaptcha_token = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(label="Contact Email", required=True, widget=widgets.TextInput())
    email_verify = forms.EmailField(label="Verify Contact Email", required=True, widget=widgets.TextInput())

    def clear_sensitive_form_data(self):
        if 'recaptcha_token' in self.cleaned_data:
            del self.cleaned_data['recaptcha_token']

    def clean_email_verify(self):
        email = self.cleaned_data['email']
        email_verify = self.cleaned_data['email_verify']
        if email != email_verify:
            raise ValidationError("Email does not match")


class EditGuestForm(StandardForm):
    guest_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'guest-id'}), required=False)
    first_name = forms.CharField(label="First Name", max_length=100, strip=True, widget=widgets.TextInput())
    last_name = forms.CharField(label="Last Name", max_length=100, strip=True, widget=widgets.TextInput())
    rsvp_answer = forms.NullBooleanField(label="Wedding Ceremony RSVP", widget=widgets.RsvpAnswerSelect())
    food_vegan_option = forms.NullBooleanField(label="Do you need a vegan food option?",
                                               widget=widgets.YesNoNullSelect())

    def __init__(self, allowed_guest_ids: list[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_guest_ids = allowed_guest_ids
        self.order_fields([
            'guest_id',
            'active',
            'first_name',
            'last_name',
            'rsvp_answer',
            'food_vegan_option'
        ])

    def clean(self):
        super().clean()
        if 'guest_id' in self.cleaned_data:
            guest_id = self.cleaned_data['guest_id']
            if guest_id and guest_id not in self.allowed_guest_ids:
                raise ValidationError("Invalid Guest ID")

    def clean_food_vegan_option(self):
        value = self.cleaned_data['food_vegan_option']
        if value is None:
            raise ValidationError("Please select Yes or No.")
        return value

    def is_deleted(self):
        return 'cleaned_data' in self and 'DELETE' in self.cleaned_data and self.cleaned_data['DELETE']


class EditGuestFormSet(forms.BaseFormSet):
    def get_deletion_widget(self):
        return forms.HiddenInput(attrs={'class': 'deletion'})
