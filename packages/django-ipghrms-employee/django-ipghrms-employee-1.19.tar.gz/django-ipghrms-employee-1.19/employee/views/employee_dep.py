import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from employee.models import Employee, Photo
from contract.models import EmpPlacement, EmpPosition
from custom.models import Department, Unit
from settings_app.user_utils import c_dep

@login_required
@allowed_users(allowed_roles=['dep'])
def UEmpDepDash(request):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	
	chief = EmpPosition.objects.filter(department=dep, position_id=4, is_active=True).first()
	staffs = EmpPlacement.objects.filter(department=dep, is_active=True).exclude(position_id=4).all()
	img = []
	if chief:
		img = Photo.objects.filter(employee=chief.employee).first()
	context = {
		'group': group, 'dep': dep, 'chief': chief, 'img': img, 'staffs': staffs, 'page': 'dep',
		'title': 'Lista Funcionariu', 'legend': 'Lista Funcionariu'
	}
	return render(request, 'employee_users/emp_dep_list.html', context)
