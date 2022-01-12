from django import forms


class UsernamePasswordForm(forms.Form):
    template_name = 'user/sign_in/user/form_username_password.html'
    username = forms.CharField(label='Username', max_length=150)
    password = forms.PasswordInput()

