from django.contrib import admin
from .models import *

@admin.register(S_Company)
class Company_admin(admin.ModelAdmin):
    list_display = ('c_name', 'c_email_id', 'approval_status', 'is_active')
    list_filter = ('approval_status',)
    actions = ['approve_companies']
    
    def approve_companies(self, request, queryset):
        queryset.update(approval_status='APPROVED', is_active = True)
admin.site.register(Auth_personal_details)
admin.site.register(C_legal_registration)
admin.site.register(C_profile_work)
admin.site.register(C_declaration)
admin.site.register(C_insurance)
admin.site.register(C_chief_technician)
