from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    title=forms.CharField(max_length=50)
    file=forms.FileField
