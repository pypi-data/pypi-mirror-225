import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import EmpSpecialize, Employee, EmpLanguage, FormalEducation, NonFormalEducation,\
	WorkExperience, EmpDependency
from employee.forms import EmpLangForm, EmpSpecialForm, FormalEduForm, NonFormalEduForm, WorkExpForm, EmpDependForm
from settings_app.utils import getnewid
from log.utils import log_action

@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpFormalEduList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = FormalEducation.objects.filter(employee=emp).all()
	context = {
		'hashid': hashid, 'emp': emp, 'objects': objects, 'group': group, 'page': "formal",
		'title': 'Edukasaun Formal', 'legend': 'Edukasaun Formal'
	}
	return render(request, 'employee2/formal_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpFormalEduDetail(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = FormalEducation.objects.get(hashed=hashid2)
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': 'formal',
		'title': 'Detalha Edukasaun Formal', 'legend': 'Detalha Edukasaun Formal'
	}
	return render(request, 'employee2/formal_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr_s','hr'])
def EmpFormalEduAdd(request, hashid, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(FormalEducation)
		form = FormalEduForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucesu.')
			return redirect('formal-edu-list', hashid=hashid)
	else: form = FormalEduForm()
	context = {
		'group': group, 'emp': emp, 'form': form, 'page': 'edu-formal',
		'title': 'Aumenta Edukasaun Formal', 'legend': 'Aumenta Edukasaun Formal'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpFormalEduUpdate(request, hashid, hashid2, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(FormalEducation, hashed=hashid2)
	if request.method == 'POST':
		form = FormalEduForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucesu.')
			return redirect('formal-edu-list', hashid=hashid)
	else: form = FormalEduForm(instance=objects)
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Altera Edukasaun Formal', 'legend': 'Altera Edukasaun Formal'
	}
	return render(request, 'employee2/form.html', context)
###
@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpNonFormalEduList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = NonFormalEducation.objects.filter(employee=emp).all()
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': 'nonformal',
		'title': 'Edukasaun Non-Formal', 'legend': 'Edukasaun Non-Formal'
	}
	return render(request, 'employee2/nonformal_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpNonFormalEduDetail(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = NonFormalEducation.objects.get(hashed=hashid2)
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': "nonformal",
		'title': 'Detalha Edukasaun Non-Formal', 'legend': 'Detalha Edukasaun Non-Formal'
	}
	return render(request, 'employee2/nonformal_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpNonFormalEduAdd(request, hashid, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(NonFormalEducation)
		form = NonFormalEduForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucesu.')
			return redirect('nonformal-edu-list', hashid=hashid)
	else: form = NonFormalEduForm()
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Aumenta Edukasaun  Non-Formal', 'legend': 'Aumenta Edukasaun  Non-Formal'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmplNonFormalEduUpdate(request, hashid, hashid2, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(NonFormalEducation, hashed=hashid2)
	if request.method == 'POST':
		form = NonFormalEduForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucesu.')
			return redirect('nonformal-edu-list', hashid=hashid)
	else: form = NonFormalEduForm(instance=objects)
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Altera Edukasaun  Non-Formal', 'legend': 'Altera Edukasaun  Non-Formal'
	}
	return render(request, 'employee2/form.html', context)
###
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpWorkExpList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = WorkExperience.objects.filter(employee=emp).all()
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': "workex",
		'title': 'Experencia Servisu', 'legend': 'Experencia Servisu'
	}
	return render(request, 'employee2/workexp_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpWorkExpDetail(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = WorkExperience.objects.get(hashed=hashid2)
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': "workex",
		'title': 'Detalha Experencia Servisu', 'legend': 'Detalha Experencia Servisu'
	}
	return render(request, 'employee2/workexp_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpWorkExpAdd(request, hashid, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(WorkExperience)
		form = WorkExpForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucesu.')
			return redirect('work-exp-list', hashid=hashid)
	else: form = WorkExpForm()
	context = {
		'group': group, 'emp': emp, 'form': form, 'page': 'workex',
		'title': 'Aumenta Experencia Servisu', 'legend': 'Aumenta Experencia Servisu'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpWorkExpUpdate(request, hashid, hashid2, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(WorkExperience, hashed=hashid2)
	if request.method == 'POST':
		form = WorkExpForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucesu.')
			return redirect('work-exp-list', hashid=hashid)
	else: form = WorkExpForm(instance=objects)
	context = {
		'group': group, 'emp': emp, 'form': form, 'page': 'workex',
		'title': 'Altera Experencia Servisu', 'legend': 'Altera Experencia Servisu'
	}
	return render(request, 'employee2/form.html', context)
###
@login_required
# @allowed_users(allowed_roles=['admin','hr','staff'])
def EmpDependList(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = EmpDependency.objects.filter(employee=emp).all()
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': "depend",
		'title': 'Lista Dependencia', 'legend': 'Lista Dependencia'
	}
	return render(request, 'employee2/depend_list.html', context)

@login_required
# @allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpDependDetail(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = EmpDependency.objects.get(hashed=hashid2)
	context = {
		'group': group, 'emp': emp, 'objects': objects, 'page': "depend",
		'title': 'Detalha Dependencia', 'legend': 'Detalha Dependencia'
	}
	return render(request, 'employee2/depend_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpDependAdd(request, hashid, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpDependency)
		form = EmpDependForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucesu.')
			return redirect('depend-list', hashid=hashid)
	else: form = EmpDependForm()
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Aumenta Dependencia', 'legend': 'Aumenta Dependencia'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpDependUpdate(request, hashid, hashid2, page):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(EmpDependency, hashed=hashid2)
	if request.method == 'POST':
		form = EmpDependForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucesu.')
			return redirect('depend-list', hashid=hashid)
	else: form = EmpDependForm(instance=objects)
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Altera Dependencia', 'legend': 'Altera Dependencia'
	}
	return render(request, 'employee2/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpLangAdd(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(EmpLanguage)
		form = EmpLangForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta sucesu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = EmpLangForm()
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Aumenta Abilidade Lingua', 'legend': 'Aumenta Abilidade Lingua'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpLangUpdate(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(EmpLanguage, hashed=hashid2)
	if request.method == 'POST':
		form = EmpLangForm(request.POST,request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucesu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = EmpLangForm(instance=objects)
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Altera Abilidade Lingua', 'legend': 'Altera Abilidade Lingua'
	}
	return render(request, 'employee2/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpSpecialAdd(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(EmpSpecialize)
		form = EmpSpecialForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.employee = emp
			instance.save()
			log_action(request, model=EmpSpecialize._meta.model_name, action="Add",field_id=instance.pk)
			messages.success(request, f'Aumenta sucesu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = EmpSpecialForm()
	context = {
		'group': group, 'emp': emp, 'form': form,
		'title': 'Aumenta Specialidade', 'legend': 'Aumenta Specialidade'
	}
	return render(request, 'employee2/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpSpecialDelete(request, hashid, pk):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	spec = get_object_or_404(EmpSpecialize, pk=pk)
	spec.delete()
	messages.success(request, f'Susesu Delete')
	return redirect('emp-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpSpecialDelete(request, hashid, pk):
	objects = get_object_or_404(EmpSpecialize, pk=pk)
	log_action(request, model=EmpSpecialize._meta.model_name, action="Delete",field_id=objects.pk)
	objects.delete()
	messages.success(request, f'Hapaga sucesu.')
	return redirect('emp-detail', hashid=hashid)
###
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def Employee2PDF(request, hashid, page):
	group = request.user.groups.all()[0].name
	if page == "formal":
		objects = get_object_or_404(FormalEducation, hashed=hashid)
	elif page == "nonformal":
		objects = get_object_or_404(NonFormalEducation, hashed=hashid)
	elif page == "depend":
		objects = get_object_or_404(EmpDependency, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')