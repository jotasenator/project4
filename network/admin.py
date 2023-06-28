from django.contrib import admin
from django import forms
from .models import User, Post, Profile


# this eliminates the user i choose in admin Profile from followers and following
# because a user can not be followed or unfollowed by himself
class ProfileAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["followers"].queryset = self.fields[
                "followers"
            ].queryset.exclude(pk=self.instance.user.pk)
            self.fields["following"].queryset = self.fields[
                "following"
            ].queryset.exclude(pk=self.instance.user.pk)


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile, ProfileAdmin)
