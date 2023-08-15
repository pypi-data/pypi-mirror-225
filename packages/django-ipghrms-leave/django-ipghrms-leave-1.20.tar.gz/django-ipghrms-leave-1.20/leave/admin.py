from django.contrib import admin
from .models import *

admin.site.register(Year)
admin.site.register(Month)

class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
admin.site.register(LeaveType, LeaveTypeAdmin)

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee','leave_type', 'description',)
    search_fields = ['employee__first_name','employee__last_name','leave_type__name', 'description',]
admin.site.register(Leave, LeaveAdmin)

class LeaveCountAdmin(admin.ModelAdmin):
    list_display = ('employee','leave_type','month','year','total_balance')
    search_fields = ['employee__first_name','employee__last_name','leave_type__name','month__name','year__year','total_balance']
admin.site.register(LeaveCount, LeaveCountAdmin)

class LeaveDelegateAdmin(admin.ModelAdmin):
    list_display = ('leave','employee',)
    search_fields = ['leave__employee__first_name','leave__employee__last_name','employee__first_name','employee__last_name',]
admin.site.register(LeaveDelegate, LeaveDelegateAdmin)

class LeaveUnitAdmin(admin.ModelAdmin):
    list_display = ('leave','obs',)
    search_fields = ['leave__employee__first_name','leave__employee__last_name','obs',]
admin.site.register(LeaveUnit, LeaveUnitAdmin)

class LeaveHRAdmin(admin.ModelAdmin):
    list_display = ('leave','obs',)
    search_fields = ['leave__employee__first_name','leave__employee__last_name','obs',]
admin.site.register(LeaveHR, LeaveHRAdmin)

class LeaveDEAdmin(admin.ModelAdmin):
    list_display = ('leave','obs',)
    search_fields = ['leave__employee__first_name','leave__employee__last_name','obs',]
admin.site.register(LeaveDE, LeaveDEAdmin)

class LeaveDepAdmin(admin.ModelAdmin):
    list_display = ('leave','obs',)
    search_fields = ['leave__employee__first_name','leave__employee__last_name','obs',]
admin.site.register(LeaveDep, LeaveDepAdmin)

class LeavePeriodAdmin(admin.ModelAdmin):
    list_display = ('employee','start_month','start_year','end_month','end_year')
    search_fields = ['employee__first_name','employee__last_name','start_month__name','start_year__year','end_month__name','end_year__year']
admin.site.register(LeavePeriod, LeavePeriodAdmin)
