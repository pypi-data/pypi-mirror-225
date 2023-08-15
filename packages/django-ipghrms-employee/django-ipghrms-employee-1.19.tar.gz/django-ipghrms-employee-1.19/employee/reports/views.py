import datetime
import employee
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from employee.models import Employee, FormalEducation
from contract.models import EmpPosition
from custom.models import Unit, Department, EducationLevel
from settings_app.user_utils import c_dep, c_unit
from settings_app.utils import getnewid, read_picture

def RAcaLevelList(request):
	group = request.user.groups.all()[0].name
	if group == 'unit':
		_, unit = c_unit(request.user)
		emps = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)), status_id=1).prefetch_related('curempdivision').all().order_by('first_name')
	elif group == 'dep':
		_, dep = c_dep(request.user)
		emps = Employee.objects.filter(curempdivision__department=dep, status_id=1).prefetch_related('curempdivision').all().order_by('first_name')
	else:
		emps = Employee.objects.filter(status_id=1).prefetch_related('curempdivision').all().order_by('first_name')
	objects = []
	for i in emps:
		a = FormalEducation.objects.filter(employee=i).last()
		objects.append([i,a])
	acalevel = EducationLevel.objects.all()
	context = {
		'group': group, 'objects': objects, 'acalevel': acalevel,
		'title': 'Lista Funcionariu baseia ba Nivel Akademiku', 'legend': 'Lista Funcionariu baseia ba Nivel Akademiku'
	}
	return render(request, 'employee_reports/aca_level_list.html', context)
