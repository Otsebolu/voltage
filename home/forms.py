# from dataclasses import fields
# from tkinter import Widget
from django import forms
from django.forms import ModelForm
from .models import * #Contact, Profile, Shopcart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name','email','message']


class SignupForm(UserCreationForm):     # creating instance.  #Links Default <USER> MODEL in Django, we dont need to put class <USER> in Models.py. See fields in <USER> Model/table at DB in the backend. 
    username = forms.CharField(max_length=50)
    first_name =forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')    #pick from field as it appears on the <User> model at the DB (pick from <ADD USER> AND LOOK AT ONE USER MODEL CREATED AND PICK ADDITIONAL ONES FROM IT, SO AS TO FORM THIS FIELDS)



STATE=[
    ('Abia', 'Abia'),
    ('Delta', 'Delta'),
    ('Edo', 'Edo'),
    ('Lagos', 'Lagos'),
    ('Ondo', 'Ondo'),
    ('Taraba', 'Taraba'),
    ('USA', 'USA'),
]

class ProfileUpdate(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name','last_name','phone','address','state','pix']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Home Address'}),
            'state': forms.Select(attrs={'class':'form-control', 'placeholder':'State'}, choices=STATE),
            'pix': forms.FileInput(attrs={'class':'form-control'}),

        }

class ShopcartForm(forms.ModelForm):
    class Meta:
        model = Shopcart
        fields = ['quantity']   #we have other fields in the other product model already. every field here is in product table except quantuty