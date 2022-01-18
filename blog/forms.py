from django import forms

from blog.models import Ad


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ['user', 'created_at', 'moderated', 'is_active']