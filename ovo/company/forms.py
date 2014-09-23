from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from .models import *
from my_user.models import CustomUser


class CompanyRegistrationForm(forms.ModelForm):
    error_css_class = "error"

    first_name = forms.CharField(max_length=100, label="name", required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    surname = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    # mobile_number = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Mobile', 'maxlength':10}))
    mobile_number = forms.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex='^\d{0,10}$',
                message='Mobile number must be a number',
                code='invalid_mobile_no'
            ),
        ]
    )

    role = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Role'}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=False)
    confirm_password = forms.CharField(max_length=100,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=False)
    number = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'N'}))
    terms = forms.BooleanField(required=False)
    register_for = forms.CharField(max_length=20,
                                   widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Company
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(CompanyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['address'] = forms.CharField(max_length=100)

    def _is_email_already_registered(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            return True
        except ObjectDoesNotExist:
            return False

    def _is_mobile_no_valid(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        try:
            con = float(mobile_number)
            return True
        except:
            return False

    def _are_all_fields_present(self):
        all_fields_present = True
        for field in self.fields.keys():
            if field not in self.cleaned_data:
                all_fields_present = False
                break
            elif not self.cleaned_data[field]:
                all_fields_present = False
                break
        return all_fields_present

    def _passwords_match(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            return False
        else:
            return True

    def clean(self):
        # if not self._are_all_fields_present():
        #     raise forms.ValidationError("Attention fill in all fields!".upper())
        if self._is_email_already_registered():
            # self.fields['email'] = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'error'}))
            raise forms.ValidationError("Email address already registered".upper())
        if not self._passwords_match():
            raise forms.ValidationError("Passwords do not match".upper())
        if not self._is_mobile_no_valid():
            raise forms.ValidationError("Mobile number not valid".upper())
        return self.cleaned_data
