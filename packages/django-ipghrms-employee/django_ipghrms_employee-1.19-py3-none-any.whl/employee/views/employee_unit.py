import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from employee.models import Employee, Photo, CurEmpDivision
from contract.models import EmpPlacement, EmpPosition
from custom.models import Department, Unit
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['unit'])
def UEmpUnitDash(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	pos = EmpPosition.objects.filter(employee=c_emp, is_active=True).first()
	img = Photo.objects.filter(employee=c_emp).first()
	deps = Department.objects.filter(unit=unit).all()
	deplist = []
	for k in deps:
		tot_dep_k = EmpPosition.objects.filter(department=k, is_active=True).all().count()
		tot_staff_dep_k = EmpPlacement.objects.filter(department=k, is_active=True).all().count()
		tot_k = tot_dep_k + tot_staff_dep_k
		deplist.append([k,tot_k])
	totdep=0
	if deplist:
		totdep = np.sum(np.array(deplist)[:,1])
	advlist = Employee.objects.filter((Q(contract__category_id=3)|Q(contract__category_id=4)),\
		(Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit))).all()
	totadv = advlist.count()
	total = totdep + totadv + 1
	context = {
		'group': group, 'unit': unit, 'c_emp': c_emp, 'pos': pos, 'img': img, 'dep': deplist,
		'totdep': totdep, 'total': total, 'page': 'unit', 'totadv': totadv,
		'title': 'Painel Pessoal', 'legend': 'Painel Pessoal'
	}
	return render(request, 'employee_users/emp_unit_dash.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmpUnitStaffList(request, pk):
	group = request.user.groups.all()[0].name
	unit = Unit.objects.get(pk=pk)
	staffs = CurEmpDivision.objects.filter(unit=unit).all()
	context = {
		'group': group, 'unit': unit, 'staffs': staffs, 'name': unit.name, 'page': 'unit',
		'title': '%s' % (unit), 'legend': '%s' % (unit)
	}
	return render(request, 'employee3/staff_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def UEmpDepList(request, pk):
	group = request.user.groups.all()[0].name
	_, unit = c_unit(request.user)
	dep = get_object_or_404(Department, pk=pk)
	chief = EmpPosition.objects.filter(department=dep, position_id=4, is_active=True).first()
	staffs = EmpPlacement.objects.filter(department=dep, is_active=True).exclude(position_id=4).all()
	img = []
	if chief:
		img = Photo.objects.filter(employee=chief.employee).first()
	context = {
		'group': group, 'dep': dep, 'chief': chief, 'img': img, 'staffs': staffs, 'page': 'unit',
		'title': 'Lista Funcionariu', 'legend': 'Lista Funcionariu'
	}
	return render(request, 'employee_users/emp_dep_list.html', context)
