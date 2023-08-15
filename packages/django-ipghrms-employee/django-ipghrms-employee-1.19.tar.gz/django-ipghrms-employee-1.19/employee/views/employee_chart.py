import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from settings_app.user_utils import c_dep, c_unit

@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmpChartDash(request):
	group = request.user.groups.all()[0].name
	_, dep = c_dep(request.user)
	_, unit = c_unit(request.user)
	title, legend = None, None
	if group == 'unit':
		legend = f'Grafiku Pessoal {unit.name}'
		context = {
			'group': group,
			'title': title, 'legend': legend
		}
		return render(request, 'employee_chart/chart_emp_unit.html', context)
	if group == 'dep':
		legend = f'Grafiku Pessoal {dep.name}'
		context = {
			'group': group,
			'title': title, 'legend': legend
		}
		return render(request, 'employee_chart/chart_emp_dep.html', context)
	else:
		title = 'Grafiku Pessoal' 
		legend = 'Grafiku Pessoal'
		context = {
			'group': group,
			'title': title, 'legend': legend
		}
		return render(request, 'employee_chart/chart_emp.html', context)