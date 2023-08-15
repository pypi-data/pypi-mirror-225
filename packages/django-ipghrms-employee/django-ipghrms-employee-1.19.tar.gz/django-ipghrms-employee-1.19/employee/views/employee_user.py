import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from employee.models import Employee, EmployeeUser, IDNumbers, LIDNumbers, IIDNumbers, ContactInfo, LocationTL,\
	AddressTL, AddressOrigin, Photo, EmployeeDivision, EmployeePosition, EmployeeDependency, FormalEducation,\
	NonFormalEducation, WorkExperience
from contract.models import InitialContract, Contract, EmployeeSalary

@login_required
# @allowed_users(allowed_roles=['staff'])
def EmployeeDetailUser(request):
	group = request.user.groups.all()[0].name
	user = EmployeeUser.objects.get(user=request.user)
	objects = Employee.objects.filter(pk=user.employee.pk).first()
	idnum = IDNumbers.objects.filter(employee=objects).first()
	lidnum = LIDNumbers.objects.filter(employee=objects).first()
	iidnum = IIDNumbers.objects.filter(employee=objects).first()
	contactinfo = ContactInfo.objects.filter(employee=objects).first()
	locationtl = LocationTL.objects.filter(employee=objects).first()
	addtl = AddressTL.objects.filter(employee=objects).first()
	addori = AddressOrigin.objects.filter(employee=objects).first()
	img = Photo.objects.filter(employee=objects).first()
	empcontract = Contract.objects.filter(employee=objects).last()
	empsalary = EmployeeSalary.objects.filter(contract=empcontract).last()
	empcontract_init = InitialContract.objects.filter(employee=objects).first()
	empposition = EmployeePosition.objects.filter(employee=objects).first()
	empdivision = EmployeeDivision.objects.filter(employee=objects).first()
	empdependency = EmployeeDependency.objects.filter(employee=objects).all()
	formaleducation = FormalEducation.objects.filter(employee=objects).last()
	nonformaleducation = NonFormalEducation.objects.filter(employee=objects).last()
	workexperience = WorkExperience.objects.filter(employee=objects).last()
	context = {
		'group': group, 'objects': objects, 'idnum': idnum, 'lidnum': lidnum, 'iidnum': iidnum,
		'contactinfo': contactinfo, 'locationtl':locationtl, 'addtl': addtl, 'addori': addori, 'img': img,
		'formaleducation': formaleducation, 'nonformaleducation': nonformaleducation, 'workexperience': workexperience,
		'empdependency': empdependency, 'empcontract': empcontract, 'empsalary': empsalary,
		'empposition': empposition, 'empdivision': empdivision,	'empcontract_init': empcontract_init,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu'
	}
	return render(request, 'employee/employee_detail.html', context)
