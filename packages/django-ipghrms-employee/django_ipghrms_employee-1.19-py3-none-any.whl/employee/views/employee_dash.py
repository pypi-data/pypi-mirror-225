import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import EmpPlacement, EmpPosition, Category
from settings_app.decorators import allowed_users
from django.db.models import Q
from employee.models import Employee
from custom.models import DE, Unit, Department
from employee.utils import get_employee_data

# @login_required
# # @allowed_users(allowed_roles=['admin','hr'])
# def EmployeeDash(request):
# 	group = request.user.groups.all()[0].name
# 	units = Unit.objects.all()
# 	deps = Department.objects.all()
# 	unitlist,deplist = [],[]
# 	for i in units:
# 		tot_unit_i = EmpPosition.objects.filter(unit=i, is_active=True).all().count()
# 		tot_staff_unit_i = EmpPlacement.objects.filter(unit=i, is_active=True).all().count()
# 		dep_ii = Department.objects.filter(unit=i).all()
# 		tot_ii = 0
# 		for ii in dep_ii:
# 			tot_dep_i = EmpPosition.objects.filter(department=ii, is_active=True).all().count()
# 			tot_staff_dep_i= EmpPlacement.objects.filter(department=ii, is_active=True).all().count()
# 			tot_ii = tot_ii + tot_dep_i + tot_staff_dep_i
# 		# tot_i = tot_ii + tot_unit_i + tot_staff_unit_i
# 		tot_i = tot_staff_unit_i
# 		unitlist.append([i,tot_i])
# 	for j in deps:
# 		tot_dep_j = EmpPosition.objects.filter(department=j, is_active=True).prefetch_related('department').count()
# 		tot_staff_dep_j = EmpPlacement.objects.filter(department=j, is_active=True).select_related('department').all().count()
# 		# tot_j = tot_dep_j + tot_staff_dep_j
# 		tot_j = tot_staff_dep_j
# 		deplist.append([j,tot_j])
# 	delist = EmpPosition.objects.filter((Q(position_id=1)|Q(position_id=2)), is_active=True).all()
# 	advlist = Employee.objects.filter((Q(contract__category_id=3)|Q(contract__category_id=4)), contract__is_active=True).all()
# 	totde = delist.count()
# 	totadv = advlist.count()
# 	totunit,totdep = 0,0
# 	if unitlist:
# 		totunit = np.sum(np.array(unitlist)[:,1])
# 	if deplist:
# 		totdep = np.sum(np.array(deplist)[:,1])
# 	total = totde + totunit + totadv
# 	context = {
# 		'group': group, 'des': delist, 'units': unitlist, 'deps': deplist, 
# 		'totadv': totadv, 'totde': totde, 'totunit': totunit, 'totdep': totdep, 'total': total,
# 		'title': 'Painel Funcionariu', 'legend': 'Painel Funcionariu'
# 	}
# 	return render(request, 'employee/emp_dash.html', context)


@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmployeeDash(request):
    group = request.user.groups.all()[0].name
    employee_data = get_employee_data()
    context = {
        'group': group, 
        'title': 'Painel Funcionariu', 
        'legend': 'Painel Funcionariu',
        **employee_data
    }
    return render(request, 'employee/emp_dash.html', context)
