from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(Status)
admin.site.register(Area)

class EmpSignatureAdmin(admin.ModelAdmin):
    list_display = ('employee',)
    search_fields = ['employee__first_name','employee__last_name',]    
admin.site.register(EmpSignature, EmpSignatureAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name',)
    search_fields = ['first_name','last_name',]    
admin.site.register(Employee, EmployeeAdmin)

class CurEmpPositionAdmin(admin.ModelAdmin):
    list_display = ('employee','position',)
    search_fields = ['employee__first_name','employee__last_name','position__name',]    
admin.site.register(CurEmpPosition, CurEmpPositionAdmin)

class CurEmpDivisionAdmin(admin.ModelAdmin):
    list_display = ('employee','de','unit','department',)
    search_fields = ['employee__first_name','employee__last_name','de__name','unit__name','department__name',]    
admin.site.register(CurEmpDivision, CurEmpDivisionAdmin)

class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ('employee','user',)
    search_fields = ['employee__first_name','employee__last_name',]    
admin.site.register(EmployeeUser, EmployeeUserAdmin)

@admin.register(EmpYear)
class EmpYearAdmin(ImportExportModelAdmin):
	pass
