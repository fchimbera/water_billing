from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['account_id', 'email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserLoginForm(forms.Form):
    account_id_or_email = forms.CharField(label='Account ID or Email')
    password = forms.CharField(widget=forms.PasswordInput)