
from django.contrib.auth.models import User
from django import forms
import re
from task.forms import StyleFormMixin


class CustomUserRegistrationForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        help_texts={
            'username':None
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'

        if len(password) < 8 :
            raise forms.ValidationError('Password must at least 8 character long')
        
        if not re.fullmatch(pattern, password):
            raise forms.ValidationError('Password must include at least one uppercase letter, one lowercase letter, one digit, and one special character (@#$%^&+=)')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match, please try again")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widget()