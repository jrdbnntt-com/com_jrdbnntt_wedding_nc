import django.forms


class TextInput(django.forms.TextInput):
    template_name = '_templates/forms/widgets/text.html'


class PasswordInput(django.forms.PasswordInput):
    template_name = '_templates/forms/widgets/password.html'

