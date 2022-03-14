from django import forms


class TextInput(forms.TextInput):
    template_name = '_templates/forms/widgets/text.html'


class PasswordInput(forms.PasswordInput):
    template_name = '_templates/forms/widgets/password.html'


class EmailInput(forms.EmailInput):
    template_name = '_templates/forms/widgets/email.html'


class Select(forms.Select):
    template_name = '_templates/forms/widgets/select.html'


class CustomChoicesBooleanSelect(Select):
    def __init__(self, attrs=None, choice_null=None, choice_true='True', choice_false='False'):
        if choice_null is None:
            choices = (
                ('true', choice_true),
                ('false', choice_false),
            )
        else:
            choices = (
                ('unknown', choice_null),
                ('true', choice_true),
                ('false', choice_false),
            )
        self.choice_null = choice_null
        super().__init__(attrs, choices)

    def format_value(self, value):
        if value is None:
            if self.choice_null is None:
                raise ValueError("Invalid value '%s', null not allowed" % str(value))
            else:
                return 'unknown',
        if value is True:
            return 'true'
        if value is False:
            return 'false'
        raise ValueError("Invalid value '%s'" % str(value))

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value is None:
            return None
        value = str(value).lower()
        if value == 'unknown':
            return None
        if value == 'true':
            return True
        if value == 'false':
            return False
        raise ValueError("Invalid value '%s'" % str(value))


class RsvpAnswerSelect(CustomChoicesBooleanSelect):
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, choice_null="TBD", choice_true="Going", choice_false="Not Going")


class YesNoSelect(CustomChoicesBooleanSelect):
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, choice_true="Yes", choice_false="No")


class YesNoNullSelect(CustomChoicesBooleanSelect):
    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, choice_null="", choice_true="Yes", choice_false="No")
