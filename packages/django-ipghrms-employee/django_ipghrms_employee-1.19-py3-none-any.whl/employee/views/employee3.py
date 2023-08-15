import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import EmpPlacement, EmpPosition
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from employee.models import Employee, FIDNumber, Photo, CurEmpDivision, CurEmpPosition
from custom.models import Department, Unit, DE
from settings_app.user_utils import c_dep, c_unit
from settings_app.utils import getnewid, read_picture

@login_required
@allowed_users(allowed_roles=['admin', 'hr'])
def EmpNoDivList(request):
	objects = Employee.objects.filter(status_id=1, curempdivision__de=None, curempdivision__unit=None,\
		curempdivision__department=None)\
		.prefetch_related('curempdivision','curempposition')
	context = {
		'objects': objects, 'page': 'nodiv',
		'title': 'Funcionariu nebe seidauk iha Divisaun', 'legend': 'Funcionariu nebe seidauk iha Divisaun'
	}
	return render(request, 'employee3/no_div_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmpDepList(request, pk):
	group = request.user.groups.all()[0].name
	dep = Department.objects.get(pk=pk)
	chief = EmpPosition.objects.filter(department=dep, is_manager=True, is_active=True).first()
	staffs = CurEmpDivision.objects.filter(department=dep).all()
	img = []
	if chief:
		img = Photo.objects.filter(employee=chief.employee).first()
	context = {
		'group': group, 'dep': dep, 'chief': chief, 'img': img, 'staffs': staffs,
		'title': '%s' % (dep), 'legend': '%s' % (dep)
	}
	return render(request, 'employee3/dep_list.html', context)
###
@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmpUnitList(request, pk):
	group = request.user.groups.all()[0].name
	unit = Unit.objects.get(pk=pk)
	deps = Department.objects.filter(unit=unit).all()
	dir = EmpPosition.objects.filter(unit=unit, position_id=3, is_active=True).first()
	staffs = EmpPlacement.objects.filter(unit=unit, is_active=True).exclude(position_id=3).all()
	objects = []
	for i in deps:
		a = EmpPosition.objects.filter(department=i, position_id=4, is_active=True).first()
		a = []
		b = EmpPlacement.objects.filter(department=i, is_active=True).exclude().all()
		objects.append([i,a,b])
	img = []
	if dir:
		img = Photo.objects.filter(employee=dir.employee).first()
	context = {
		'group': group, 'unit': unit, 'dir': dir, 'img': img, 'staffs': staffs, 'objects': objects,
		'title': '%s' % (unit), 'legend': '%s' % (unit)
	}
	return render(request, 'employee3/unit_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def EmpUnitStaffList(request, pk):
# 	group = request.user.groups.all()[0].name
# 	unit = Unit.objects.get(pk=pk)
# 	staffs = EmpPlacement.objects.filter(unit=unit, is_active=True).all()
# 	context = {
# 		'group': group, 'unit': unit, 'staffs': staffs, 'name': unit.name, 'page': 'unit',
# 		'title': '%s' % (unit), 'legend': '%s' % (unit)
# 	}
# 	return render(request, 'employee3/staff_list.html', context)
###
@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def AdvList(request):
	group = request.user.groups.all()[0].name
	objects = []
	if group == 'unit':
		_, unit = c_unit(request.user)
		objects = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
		(Q(contract__category_id=3) | Q(contract__category_id=4)), contract__is_active=True).all()
	elif group == 'dep':
		_, dep = c_dep(request.user)
		objects = Employee.objects.filter((Q(contract__category_id=3)|Q(contract__category_id=4)),\
			curempdivision__department=dep, contract__is_active=True).all()
	else:
		objects = Employee.objects.filter((Q(contract__category_id=3) | Q(contract__category_id=4)),\
		contract__is_active=True).all()
	context = {
		'objects': objects,
		'title': 'Lista Assessor', 'legend': 'Lista Assessor'
	}
	return render(request, 'employee3/adv_list.html', context)
###