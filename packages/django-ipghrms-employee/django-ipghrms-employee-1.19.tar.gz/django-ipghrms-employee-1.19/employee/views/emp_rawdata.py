from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary
from settings_app.decorators import allowed_users
from django.db.models import Q
from employee.models import CurEmpDivision, CurEmpPosition, Employee, FIDNumber, FormalEducation, FormalEducation


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EmpRawData(request):
	group = request.user.groups.all()[0].name
	objects = []
	emps = Employee.objects.filter(contract__contract_type_id=1).prefetch_related('contract')\
		.all().order_by('curempposition__position__id')
	for i in emps:
		fidnum = FIDNumber.objects.filter(employee=i).first()
		cont = Contract.objects.filter(employee=i, is_active=True).last()
		salary = EmpSalary.objects.filter(contract=cont).first()
		emppos = CurEmpPosition.objects.filter(employee=i).first()
		empdiv = CurEmpDivision.objects.filter(employee=i).first()
		formedu = FormalEducation.objects.filter(employee=i)
		objects.append([i,fidnum,cont,salary,empdiv,emppos,formedu])
	context = {
		'group': group, 'objects': objects,
		'title': 'Employees Raw Data', 'legend': 'Employees Raw Data'
	}
	return render(request, 'employee3/raw_data_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def AdvisorRawData(request):
	group = request.user.groups.all()[0].name
	objects = []
	emps = Employee.objects.exclude(contract__contract_type_id=1).prefetch_related('contract')\
		.all().order_by('first_name','last_name')
	for i in emps:
		fidnum = FIDNumber.objects.filter(employee=i).first()
		cont = Contract.objects.filter(employee=i, is_active=True).last()
		salary = EmpSalary.objects.filter(contract=cont).first()
		emppos = CurEmpPosition.objects.filter(employee=i).first()
		empdiv = CurEmpDivision.objects.filter(employee=i).first()
		formedu = FormalEducation.objects.filter(employee=i).last()
		objects.append([i,fidnum,cont,salary,empdiv,emppos,formedu])
	context = {
		'group': group, 'objects': objects,
		'title': 'Advisors Raw Data', 'legend': 'Advisors Raw Data'
	}
	return render(request, 'employee3/raw_data_advisor.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def HabiRawData(request):
	objects = []
	objs = FormalEducation.objects.filter().all().order_by('employee__first_name','-graduation_year')
	for i in objs:
		fidnum = FIDNumber.objects.filter(employee=i.employee).first()
		cont = Contract.objects.filter(employee=i.employee, is_active=True).last()
		emppos = CurEmpPosition.objects.filter(employee=i.employee).first()
		empdiv = CurEmpDivision.objects.filter(employee=i.employee).first()
		objects.append([i.employee,fidnum,cont,empdiv,emppos,i])
	context = {
		'objects': objects,
		'title': 'Literary Qualification', 'legend': 'Literary Qualification'
	}
	return render(request, 'employee3/raw_data_habi.html', context)
