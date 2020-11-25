from django.contrib import admin
from django.db import models as django_models
from django.forms import TextInput


from . import models


@admin.register(models.Requests)
class RequestsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    formfield_overrides = {
        django_models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }
    list_display = ('created_at', 'user', 'status')
    list_filter = ('user', 'status')


class AssignedRolesInline(admin.TabularInline):
    model = models.AssignedRoles
    extra = 1


@admin.register(models.ExtendingUser)
class ExtendingUserAdmin(admin.ModelAdmin):
    inlines = [AssignedRolesInline]
    list_display = ('user',)


@admin.register(models.UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('role_name',)
