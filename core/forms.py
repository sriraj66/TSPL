from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Username',
            'required': "true",
            "autocomplete": "off"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Password',
            'required': "true",
            "autocomplete": "off"
        })
    )

class RegisterForm(UserCreationForm):
    username = forms.EmailField(
        label="Username or Email ",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ie , ...@gmail.com'
        })
    )
    
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


from django import forms
from .models import PlayerRegistration

class PlayerRegistrationForm(forms.ModelForm):
    class Meta:
        model = PlayerRegistration
        fields = [
            'registration_category',
            'player_name',
            'father_name',
            'mother_name',
            'dob',
            'gender',
            'tshirt_size',
            'mobile',
            'emergency_mobile',
            'email',
            'adhar_card',
            'player_image',
            'district',
            'pin_code',
            'address',
            'level',
            'bowling_arm',
            'bowling_pace',
            'first_preference',
            'captain_exp',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'player_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adhar_card': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'player_image' : forms.FileInput(attrs={'class':'form-control',"name":"formFile","accept" : "image/*"}),
            'pin_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'registration_category': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'tshirt_size': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'bowling_arm': forms.Select(attrs={'class': 'form-control'}),
            'bowling_pace': forms.Select(attrs={'class': 'form-control'}),
            'first_preference': forms.Select(attrs={'class': 'form-control'}),
            'captain_exp': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'registration_category': 'Registration Category',
            'player_name': 'Player Name',
            'father_name': 'Father\'s Name',
            'mother_name': 'Mother\'s Name',
            'dob': 'Date of Birth',
            'gender': 'Gender',
            'tshirt_size': 'T-Shirt Size',
            'mobile': 'Mobile Number',
            'emergency_mobile': 'Emergency Mobile Number',
            'email': 'Email Address',
            'adhar_card': 'Aadhar Card Number',
            'player_image': 'Player Image',
            'district': 'District',
            'pin_code': 'PIN Code',
            'address': 'Address',
            'level': 'Player Level',
            'bowling_arm': 'Bowling Arm',
            'bowling_pace': 'Bowling Pace',
            'first_preference': 'First Preference',
            'captain_exp': 'Captain Experience',
        }
