from django import forms


class TextInput(forms.TextInput):
    template_name = '_templates/forms/widgets/text.html'


class PasswordInput(forms.PasswordInput):
    template_name = '_templates/forms/widgets/password.html'


class EmailInput(forms.EmailInput):
    template_name = '_templates/forms/widgets/email.html'


class Select(forms.Select):
    template_name = '_templates/forms/widgets/select.html'


class RsvpAnswerSelect(Select):
    def __init__(self, attrs=None):
        choices = (
            ('unknown', 'TBD'),
            ('true', 'Going'),
            ('false', 'Not Going'),
        )
        super().__init__(attrs, choices)

    def format_value(self, value):
        try:
            return {
                True: 'true', False: 'false',
                'true': 'true', 'false': 'false',
                # For backwards compatibility with Django < 2.2.
                '2': 'true', '3': 'false',
            }[value]
        except KeyError:
            return 'unknown'

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        return {
            True: True,
            'True': True,
            'False': False,
            False: False,
            'true': True,
            'false': False,
            # For backwards compatibility with Django < 2.2.
            '2': True,
            '3': False,
        }.get(value)
