from django.contrib import admin
from django import forms

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import MyUser, UserProfile



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'mobile_number', 'email', 'is_admin')
    list_filter = ('is_admin','is_active', 'mobile_number')
    list_display_links = ('id', 'username', 'mobile_number')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'mobile_number')
    ordering = ('username',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname',)
    list_display_links = ( 'id', 'firstname',)

admin.site.register(MyUser, UserAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
