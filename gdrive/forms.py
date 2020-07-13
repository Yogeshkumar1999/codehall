from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserFiles, Customer

class FilesForm(ModelForm):
    class Meta:
        model = UserFiles
        fields = '__all__'
        exclude = ['customer', 'name']

class AllFilesForm(ModelForm):
    name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Search for the file...'}))

    class Meta:
        model = UserFiles
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fileds = '__all__'
        exclude = ['user']
