from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
import pyotp

from .models import UserPSK

admin.site.unregister(User)


class UserPSKInline(admin.StackedInline):
    model = UserPSK
    readonly_fields = ('qr_code',)

    def qr_code(self, instance):
        totp = pyotp.TOTP(instance.secret_key)
        return mark_safe('<img src="https://chart.googleapis.com/chart?cht=qr&amp;chs=128x128&amp;chl={}" alt="{}" />'.format(totp.provisioning_uri(name='{}@django-demo'.format(instance.user.username)), instance.secret_key))


class UserProfileAdmin(UserAdmin):
    inlines = [UserPSKInline]

admin.site.register(User, UserProfileAdmin)
