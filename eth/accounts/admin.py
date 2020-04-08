from django.contrib import admin
from .models import GuestEmail

from django.contrib.auth import get_user_model

from .forms import UserAdminCreationForm, UserAdminChangeForm

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.conf import settings

# User = settings.AUTH_USER_MODEL

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','full_name','admin','staff','active')
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff','active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()



admin.site.register(User, UserAdmin)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

# class UserAdmin(admin.ModelAdmin):
# 	search_fields = ['email']
# 	form = UserAdminChangeForm  # update view
# 	add_form = UserAdminCreationForm # create view

	# class Meta:
	# 	model = User 



# admin.site.register(User, UserAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
	search_fields = ['email']
	class Meta:
		model = GuestEmail 

admin.site.register(GuestEmail, GuestEmailAdmin)