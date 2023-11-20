from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
# ------------------------------------------------
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
      model = CustomUser
      fields = ('email','image_url')
      
    def clean_password2(self):
        password1= self.cleaned_data.get("password1")
        password2= self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords do not match")  
        return password1
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user      
# ------------------------------------------------
class RegisterUserForm(forms.Form):
    email=forms.EmailField(label="",
                           error_messages={'required':'This field cannot be empty','invalid':'This email is not valid!'},
                           widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your mail'}))
    password=forms.CharField(label="",
                             widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'}))
    confirm_password=forms.CharField(label="",
                                     widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password again'}))
    image_url=forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your image address'}))
#<-------- check the email and number not Repetitious  ----------->  
    def clean_email(self):
        email=self.cleaned_data['email']
        flag=CustomUser.objects.filter(email=email).exists()
        if flag:
            raise ValidationError('This mail already exists!')
        return email
    
    def clean(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Password and confirm password are different')
    
# -----------------------------------------------
class LoginUserForm(forms.Form):
    email = forms.EmailField(label="",
                             error_messages={'required':'This field cannot be empty',
                                           'invalid':'This email is not valid!'},
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your mail'}))  
    password=forms.CharField(label="",
                             widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'}))
