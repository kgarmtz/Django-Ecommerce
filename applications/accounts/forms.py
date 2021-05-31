from django import forms
from .models import Account

# Creating a form that depends on a model
class RegistrationForm(forms.ModelForm):
    # Custom fields are not explicit declared in our model, so the value
    # we give to them won't be saved in the dabase, at least we want it. 
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    # This function initializes the form before it gets sent to the template
    def __init__(self, *args, **kwargs):
        # self.fields is populated after __init__ of ModelForm has executed, so before
        # we make any changes to self.fields, we have to call superclass __init__ 
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        # Looping through all the form fields and assign them the same class
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    # When are performing a validation on more than one field at a time, the 
    # best approach is using the clean method
    def clean(self):
        # Calling the superclass clean() method in order to obtain the cleaned_data
        # that has all the form fields that have been previously validated. 
        cleaned_data = super(RegistrationForm, self).clean()
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # Verifying whether the passwords match or not
        if password != confirm_password:
            raise forms.ValidationError('Passwords have to match!')
