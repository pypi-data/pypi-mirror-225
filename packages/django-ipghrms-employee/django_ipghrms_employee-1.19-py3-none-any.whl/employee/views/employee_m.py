import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from employee.models import Employee, FIDNumber, FIDNumber, LIDNumber, IIDNumber, ContactInfo,\
    LocationTL, AddressTL, LocationInter, Photo, EmployeeUser, DriverLicence, EmpSignature
from employee.forms import EmployeeForm, FIDNumberForm, LIDNumberForm, IIDNumberForm, ContactInfoForm,\
	LocationTLForm, AddressTLForm, LocationInterForm, PhotoForm, EmpStatusForm,EmpSignatureForm, DriverLicenceForm, PasswordForm
from settings_app.utils import getnewid, split_string
from contract.models import EmpSalary
from django.contrib.auth.hashers import check_password
from log.utils import log_action

from ipware import get_client_ip

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeAdd(request):
	group = Group.objects.get(name='staff')
	if request.method == 'POST':
		newid, new_hashid = getnewid(Employee)
		newid2, _ = getnewid(User)
		newid3, _ = getnewid(EmployeeUser)
		form = EmployeeForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.status_id = 1
			instance.datetime = datetime.datetime.now()
			instance.hashed = new_hashid
			instance.user = request.user
			instance.save()
			username = split_string(form.cleaned_data.get('first_name')).lower()+str(newid)
			password = make_password('ipghrms')
			obj = User(id=newid2, username=username, password=password)
			obj.save()
			obj2 = EmployeeUser(id=newid3, user_id=newid2, employee_id=newid)
			obj2.save()
			user = User.objects.get(pk=newid2)
			user.groups.add(group)
			messages.success(request, f'Aumenta sucessu.')
			return redirect('emp-detail', instance.hashed)
	else: form = EmployeeForm()
	context = {
		'form': form,
		'title': 'Aumenta Funcionariu', 'legend': 'Aumenta Funcionariu'
	}
	return render(request, 'employee/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeUpdate(request, hashid):
	objects = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			log_action(request, model=Employee._meta.model_name, action="Update",field_id=objects.pk)
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = EmployeeForm(instance=objects)
	context = {
		'form': form,
		'title': 'Altera Funcionariu', 'legend': 'Altera Funcionariu'
	}
	return render(request, 'employee/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def FIDNumberUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = FIDNumber.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = FIDNumberForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			# log_action(request, model=FIDNumber._meta.model_name, action="Update",field_id=objects.pk)
			log_action(request, model="finance", action="Update",field_id=objects.pk)
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = FIDNumberForm(instance=objects)
	context = {
		'group':group, 'form': form, 'emp': emp,
		'title': 'Altera ID Financeiru', 'legend': 'Altera ID Financeiru'
	}
	return render(request, 'employee/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LIDNumberUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = LIDNumber.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = LIDNumberForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = LIDNumberForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera ID Nacional', 'legend': 'Altera ID Nacional'
	}
	return render(request, 'employee/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def IIDNumberUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = IIDNumber.objects.filter(employee=emp).first()

	if request.method == 'POST':
		form = IIDNumberForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = IIDNumberForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera ID Internacional', 'legend': 'Altera ID Internacional'
	}
	return render(request, 'employee/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def ContactInfoUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = ContactInfo.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = ContactInfoForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = ContactInfoForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Kontaktu', 'legend': 'Altera Informasaun Kontaktu'
	}
	return render(request, 'employee/form3.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LocationTLUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = LocationTL.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = LocationTLForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = LocationTLForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Naturalidade', 'legend': 'Altera Naturalidade'
	}
	return render(request, 'employee/form_location.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AddressTLUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = AddressTL.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = AddressTLForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = AddressTLForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Enderesu', 'legend': 'Altera Enderesu iha Timor Leste'
	}
	return render(request, 'employee/form_address.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LocationInterUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = LocationInter.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = LocationInterForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = LocationInterForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Enderesu Internacional', 'legend': 'Altera Enderesu Internacional'
	}
	return render(request, 'employee/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def PhotoUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	img = Photo.objects.get(employee=emp)
	if request.method == 'POST':
		form = PhotoForm(request.POST, request.FILES, instance=img)
		if form.is_valid():
			if request.FILES:
				form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
		else:
			messages.error(request, f'Error Iha Imagen, Hilo favor hili Imagen ho Kapasidade Kiik < 0.5MB')
	else: form = PhotoForm()
	context = {
		'hashid': hashid, 'emp': emp, 'img': img, 'form': form,
		'legend': 'Upload Imajen', 'title': 'Upload Imajen',
	}
	return render(request, 'employee/emp_photo.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def DriverLicenceUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = DriverLicence.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = DriverLicenceForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = DriverLicenceForm(instance=objects)
	context = {
		'hashid': hashid, 'emp': emp, 'form': form,
		'title': 'Altera Karta Kondusaun', 'legend': 'Altera Karta Kondusaun'
	}
	return render(request, 'employee/form2.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def StatusUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		form = EmpStatusForm(request.POST, instance=emp)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid=hashid)
	else: form = EmpStatusForm(instance=emp)
	context = {
		'hashid': hashid, 'emp': emp, 'form': form,
		'title': 'Altera Status', 'legend': 'Altera StatusStatus'
	}
	return render(request, 'employee/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeIsNew(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	emp.is_new = True
	emp.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('emp-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeIsOld(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	emp.is_new = False
	emp.save()
	messages.success(request, f'Altera sucessu.')
	return redirect('emp-detail', hashid=hashid)


# ASK PASSWORD MODAL
@login_required
def CheckPassword(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	empSalary = EmpSalary.objects.filter(employee=emp, is_active=True).last()
	if request.method == 'POST':
		entered_password = request.POST.get('password')
		user = User.objects.get(pk=request.user.pk)
		if check_password(entered_password, user.password):
			context = {
				'page': 'pass'
			}
			return redirect('salary-detail', empSalary.hashed)
		else:
			messages.error(request, 'Password Sala!!')
			return redirect('emp-detail', emp.hashed)
		

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeAddSignature(request, hashid):
	employee = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(EmpSignature)
		form = EmpSignatureForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.employee = employee
			instance.id = newid
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('emp-detail', hashid)
	else: form = EmpSignatureForm()
	context = {
		'form': form,
		'title': 'Aumenta Asinatura', 'legend': 'Aumenta Asinatura'
	}
	return render(request, 'employee/form.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmployeeUpdateSignature(request, hashid, pk):
	signature = get_object_or_404(EmpSignature, pk=pk)
	if request.method == 'POST':
		form = EmpSignatureForm(request.POST, request.FILES, instance=signature)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('emp-detail', hashid)
	else: form = EmpSignatureForm(instance=signature)
	context = {
		'form': form,
		'title': 'Altera Asinatura', 'legend': 'Altera Asinatura'
	}
	return render(request, 'employee/form.html', context)

