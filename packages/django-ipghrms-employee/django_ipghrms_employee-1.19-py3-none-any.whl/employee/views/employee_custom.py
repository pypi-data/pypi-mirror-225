from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from custom.models import University, EducationLevel
from employee.forms import EmpCusUniForm, EmpCusAreaForm, EmpCusEduLevelForm
from employee.models import Employee, Area


@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s', 'de', 'deputy'])
def EmpCustomUniversityList(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	objects = University.objects.all().order_by('name')
	context = {
		'objects': objects, 'page': 'uni-list', 'employee':employee,
		'title': 'Lista Universidade', 'legend': 'Lista Universidade', 
		'title_p': f' <center> <h2>LISTA UNIVERSIDADE</h2> </center>',
		'page3': "formal",
	}
	return render(request, 'employee_custom/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomUniversityAdd(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusUniForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('custom-uni-list', employee.hashed)
	else: form = EmpCusUniForm()
	context = {
		'form': form, 'page': 'add-university','employee':employee,
		'title': 'Aumenta Universidade', 'legend': 'Aumenta Universidade'
	}
	return render(request, 'employee_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomUniversityUpdate(request, pk, hashid):
	objects = get_object_or_404(University, pk = pk)
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusUniForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('custom-uni-list', employee.hashed)
	else: form = EmpCusUniForm(instance=objects)
	context = {
		'form': form, 'page': 'add-university','employee':employee,
		'title': 'Altera Universidade', 'legend': 'Altera Universidade'
	}
	return render(request, 'employee_custom/form.html', context)




##AREA
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s', 'de', 'deputy'])
def EmpCustomAreaList(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	objects = Area.objects.all().order_by('name')
	context = {
		'objects': objects, 'page': 'uni-list', 'employee':employee,
		'title': 'Lista Area', 'legend': 'Lista Area', 'page3': "formal",
		'title_p': f' <center> <h2>LISTA AREA</h2> </center>'
	}
	return render(request, 'employee_custom/area_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomAreaAdd(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusAreaForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('custom-area-list', employee.hashed)
	else: form = EmpCusAreaForm()
	context = {
		'form': form, 'page': 'add-area','employee':employee,
		'title': 'Aumenta Area', 'legend': 'Aumenta Area'
	}
	return render(request, 'employee_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomAreaUpdate(request, pk, hashid):
	objects = get_object_or_404(Area, pk = pk)
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusUniForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('custom-area-list', employee.hashed)
	else: form = EmpCusUniForm(instance=objects)
	context = {
		'form': form, 'page': 'add-area','employee':employee,
		'title': 'Altera Area', 'legend': 'Altera Area'
	}
	return render(request, 'employee_custom/form.html', context)


## EDUCATION
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s', 'de', 'deputy'])
def EmpCustomEduLevelList(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	objects = EducationLevel.objects.all().order_by('name')
	context = {
		'objects': objects, 'page': 'uni-list',
		'page2': 'edu-list', 
		'employee':employee,
		'title': 'Lista Nivel Edukasaun', 'legend': 'Lista Nivel Edukasaun', 
		'title_p': f' <center> <h2>LISTA NIVEL EDUKASAUN</h2> </center>',
		'page3': "formal",
	}
	return render(request, 'employee_custom/edu_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomEduLevelAdd(request, hashid):
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusEduLevelForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('custom-edu-list', employee.hashed)
	else: form = EmpCusEduLevelForm()
	context = {
		'form': form, 'page': 'add-edu','employee':employee,
		'title': 'Aumenta Nivel Edukasaun', 'legend': 'Aumenta Nivel Edukasaun'
	}
	return render(request, 'employee_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpCustomEduLevelUpdate(request, pk, hashid):
	objects = get_object_or_404(EducationLevel, pk = pk)
	employee = get_object_or_404(Employee,  hashed=hashid)
	if request.method == 'POST':
		form = EmpCusEduLevelForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('custom-edu-list', employee.hashed)
	else: form = EmpCusEduLevelForm(instance=objects)
	context = {
		'form': form, 'page': 'add-edu','employee':employee,
		'title': 'Altera Nivel Edukasaun', 'legend': 'Altera Nivel Edukasaun'
	}
	return render(request, 'employee_custom/form.html', context)