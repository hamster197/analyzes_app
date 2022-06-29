from django.contrib import admin
# Register your models here.

from .models import *
from django.contrib.auth.admin import UserAdmin



class UserAdmin(UserAdmin):
    list_display = ('pk', 'username','first_name', 'last_name', 'email','is_superuser','is_staff','is_active','last_login',)
    list_editable = ('is_active','is_superuser','is_staff')
    list_filter = ('is_superuser','is_active','is_staff','last_login')
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name','patronymic', 'last_name', 'phone', 'email', 'password',  'gender',
                       'groups', 'is_active',)
        }),
        ('Patient options', {
            'classes': ('collapse',),
            'fields': ('age', 'height', 'weight', 'sport',)
        }),
        ('Doctors options', {
            'classes': ('collapse',),
            'fields': ('position', 'photo', )
        }),
    )

admin.site.register(User, UserAdmin, )

admin.site.register(SportQuide)
admin.site.register(DoctorsPositionQuide)

class ChemicalElementsMainQuideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'data_min', 'data_max', 'must_not_contain',)
    list_editable = ('data_min', 'data_max', 'must_not_contain',)

admin.site.register(ChemicalElementsMainQuide, ChemicalElementsMainQuideAdmin)

class RecomendationsQuideAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'creation_date', 'type')
    list_filter = ('patient', 'type')

admin.site.register(RecomendationsQuide, RecomendationsQuideAdmin)

class PatirntAnalizlerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'creation_date', 'patient', 'eliment', 'rezult', )
    list_filter = ('patient',)

admin.site.register(PatirntAnalizler, PatirntAnalizlerAdmin)