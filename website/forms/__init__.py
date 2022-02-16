from django import forms
import django.middleware.csrf


class StandardForm(forms.Form):
    template_name = '_templates/forms/layout/standard.html'
