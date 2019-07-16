from django import forms


class GetTokenForm(forms.Form):
    username = forms.CharField(max_length=20, )
