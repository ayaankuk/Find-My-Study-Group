from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ALLOWED_DOMAINS = ('mylaurier.ca', 'wlu.ca')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if '@' not in email:
            raise forms.ValidationError('Enter a valid Laurier email address.')
        domain = email.split('@')[-1]
        if domain not in ALLOWED_DOMAINS:
            raise forms.ValidationError('Please use your Wilfrid Laurier email (@mylaurier.ca or @wlu.ca).')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
