from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate
from django.shortcuts import redirect

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
    def clean_email(self):
      email = self.cleaned_data.get('email')
      if CustomUser.objects.filter(email=email).exists():
        raise forms.ValidationError("Email is already taken.")
      return email
      
    def clean_phone_number(self):
      phone_number = self.cleaned_data.get('phone_number')
      if CustomUser.objects.filter(phone_number=phone_number).exists():
        raise forms.ValidationError('Phone number is already registered.')
      return phone_number
    
    def clean(self):
      cleaned_data = super().clean()
      return cleaned_data
      
      
class LoginForm(forms.Form):
  username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  
  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is None:
      raise forms.ValidationError('Invalid username or password.')
      
    self.user = user  
    return cleaned_data
    


