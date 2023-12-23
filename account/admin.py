''' Developer : #ABS '''

from django.contrib import admin
from .models import user_accounts


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_login', 'phoneNumber', 'is_staff',)
    list_filter = ( 'email', 'is_superuser',  'is_staff',  'first_name', 'status')
    search_fields = ('all',)


admin.site.register(user_accounts, AccountsAdmin)
