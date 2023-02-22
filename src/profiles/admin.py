from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from .models import QueUser, SocialLink, Education, UserAPIKeyModel


@admin.register(QueUser)
class QueUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Info'),
         {'fields': (
             'phone', 'smart_photos', 'birthday', 'city',
             'bio', 'gender', 'is_verified')}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('spotify', 'instagram')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('education',)


@admin.register(UserAPIKeyModel)
class UserAPIKeyBModelAdmin(APIKeyModelAdmin):
    pass
