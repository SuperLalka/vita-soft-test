from django.contrib import admin
from django.db import models as django_models
from django.forms import TextInput


from . import models


@admin.register(models.Requests)
class CategoriesAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    formfield_overrides = {
        django_models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }
    list_display = ('creation_date', 'user', 'status')
    list_filter = ('user', 'status')


@admin.register(models.ExtendingUser)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_user', 'is_operator', 'is_admin')
    list_filter = ('is_user', 'is_operator', 'is_admin')
