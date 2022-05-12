from django.db.models import Q
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import MyUser, UserProfile


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Mobile_Number / Email', widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")
        user_qs_final = MyUser.objects.filter(
                Q(mobile_number__iexact=query)|
                Q(email__iexact=query)
            ).distinct()
        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError("Invalid credentials -- user does not exists")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid credentials")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': "form-control"}))
    mobile_number = forms.CharField(label='Mobile Number', widget=forms.TextInput(attrs={'class': "form-control"}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = MyUser
        fields = (
            'email',
            'mobile_number',
            'username',
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = (
            'email',
            'mobile_number',
            'username',
            'password',
            'is_active',
            'is_admin'
            )

    def clean_password(self):
        return self.initial["password"]


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = MyUser
        fields = ("email",'mobile_number','username')

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = MyUser
        fields = (
            'email',
            'mobile_number',
            'username',
            'password',
            'is_active',
            'is_admin'
            ) 
    