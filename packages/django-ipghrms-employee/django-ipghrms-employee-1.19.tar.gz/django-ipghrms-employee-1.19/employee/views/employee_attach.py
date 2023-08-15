import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import employee
from settings_app.decorators import allowed_users
from django.db.models import Q
from employee.models import Employee, IIDNumber, LIDNumber,FormalEducation, NonFormalEducation,\
	EmpDependency, DriverLicence
from contract.models import Contract, EmpPosition

@login_required
def EmployeeAttachment(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Employee, hashed=hashid)
	idnum = IIDNumber.objects.filter(employee=objects).first()
	lidnum = LIDNumber.objects.filter(employee=objects).first()
	driver = DriverLicence.objects.filter(employee=objects).first()
	empcontract = Contract.objects.filter(employee=objects, is_active=True).last()
	empposition = EmpPosition.objects.filter(employee=objects, is_active=True).last()
	empdepend = EmpDependency.objects.filter(employee=objects).all()
	formaledu = FormalEducation.objects.filter(employee=objects).all()
	nonformaledu = NonFormalEducation.objects.filter(employee=objects).all()
	
	context = {
		'group': group, 'emp': objects, 'idnum': idnum, 'lidnum': lidnum, 'driver': driver,
		'empcontract': empcontract, 'empposition':empposition,
		'empdepend': empdepend, 'formaledu': formaledu, 'nonformaledu': nonformaledu,
		'estado': 'estado', 'bank': 'bank', 'cert': 'cert', 'el': 'el', 'bi': 'bi', 'pas': 'pas', 'position':'position',
		'driv': 'driv', 'pdepend': 'dependency', 'pformal': 'formal', 'pnonformal': 'nonformal', 'contract': 'contract',
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu', 'employee':objects, 'page': 'attach'
	}
	return render(request, 'employee/emp_attach.html', context)

@login_required
def SEmployeeAttachment(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Employee, hashed=hashid)
	idnum = IIDNumber.objects.filter(employee=objects).first()
	lidnum = LIDNumber.objects.filter(employee=objects).first()
	driver = DriverLicence.objects.filter(employee=objects).first()
	empcontract = Contract.objects.filter(employee=objects, is_active=True).last()
	empdepend = EmpDependency.objects.filter(employee=objects).all()
	formaledu = FormalEducation.objects.filter(employee=objects).all()
	nonformaledu = NonFormalEducation.objects.filter(employee=objects).all()
	
	context = {
		'group': group, 'emp': objects, 'idnum': idnum, 'lidnum': lidnum, 'driver': driver,
		'empcontract': empcontract,
		'empdepend': empdepend, 'formaledu': formaledu, 'nonformaledu': nonformaledu,
		'estado': 'estado', 'bank': 'bank', 'cert': 'cert', 'el': 'el', 'bi': 'bi', 'pas': 'pas',
		'driv': 'driv', 'pdepend': 'dependency', 'pformal': 'formal', 'pnonformal': 'nonformal',
		'title': 'Ita Nia Anekso', 'legend': 'Ita Nia Anekso', 'employee':objects, 'page': 'attach'
	}
	return render(request, 'employee/s_emp_attach.html', context)

from django.conf import settings
from django.http import FileResponse, Http404
@login_required
def EmployeeLIDNumPDF(request, hashid, page):
	emp = get_object_or_404(Employee, hashed=hashid)
	lid = LIDNumber.objects.get(employee=emp)
	driver = DriverLicence.objects.filter(employee=emp).first()
	idnum = IIDNumber.objects.filter(employee=emp).first()
	cont = Contract.objects.filter(employee=emp).last()
	pos = EmpPosition.objects.filter(employee=emp, is_active=True).last()
	if page == 'el':
		file = str(settings.BASE_DIR)+str(lid.file_el.url)
	elif page == 'cert':
		file = str(settings.BASE_DIR)+str(lid.file_cert.url)
	elif page == 'bi':
		file = str(settings.BASE_DIR)+str(lid.file_bi.url)
	elif page == 'pas':
		file = str(settings.BASE_DIR)+str(lid.file_pas.url)
	elif page == 'driv':
		file = str(settings.BASE_DIR)+str(driver.file.url)
	elif page == 'bank':
		file = str(settings.BASE_DIR)+str(idnum.file.url)
	elif page == 'estado':
		file = str(settings.BASE_DIR)+str(lid.file_civil.url)
	elif page == 'contract':
		file = str(settings.BASE_DIR)+str(cont.file.url)
	elif page == 'position':
		file = str(settings.BASE_DIR)+str(pos.file.url)
	try:
		if file:
			return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else:
			return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')
