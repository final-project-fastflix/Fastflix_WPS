from django import forms

class UserCreateForm(forms.Form):
    name = forms.CharField(max_length=20, )
    # birth = forms.DateField()
    password = forms.PasswordInput()
