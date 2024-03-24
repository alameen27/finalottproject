# forms.py
from datetime import date

from django import forms
from django.forms import PasswordInput

from .models import Customer
from .models import CustomerProfile, KidProfile


class KidProfileForm(forms.ModelForm):
    class Meta:
        model = KidProfile
        fields = ['profilename', 'avatar']


class CustomerRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'username', 'password', 'confirm_password', 'DoB', 'phonenumber']

        widgets = {
            'DoB': forms.DateInput(attrs={'type': 'date'}),
            'password': PasswordInput(render_value=True),
        }

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if any(char.isdigit() for char in firstname):
            raise forms.ValidationError('First name should not contain numbers.')
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        if any(char.isdigit() for char in lastname):
            raise forms.ValidationError('Last name should not contain numbers.')
        return lastname

    def clean_DoB(self):
        dob = self.cleaned_data['DoB']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 12:
            raise forms.ValidationError('You must be 12 years or older to register.')

        return dob

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must match.")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerProfileForm(forms.ModelForm):
    confirm_pin = forms.CharField(widget=forms.PasswordInput, label='Confirm PIN')
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerProfile
        fields = ['profilename', 'pin', 'confirm_pin', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        confirm_pin = cleaned_data.get('confirm_pin')

        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PIN and Confirm PIN do not match.")

class PINVerificationForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput, label='')


class EditProfileForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerProfile
        fields = ['profilename', 'pin', 'avatar']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Set initial values for the fields based on the instance
        if self.instance:
            self.initial['profilename'] = self.instance.profilename
            self.initial['pin'] = self.instance.pin
            self.initial['avatar'] = self.instance.avatar

class KidProfileForm(forms.ModelForm):
    class Meta:
        model = KidProfile
        fields = ['profilename', 'avatar']