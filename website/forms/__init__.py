from django import forms


class StandardForm(forms.Form):
    template_name = '_templates/forms/layout/standard.html'
