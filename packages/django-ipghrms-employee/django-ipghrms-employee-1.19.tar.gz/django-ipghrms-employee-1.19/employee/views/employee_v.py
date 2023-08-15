from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary, EmpPlacement
from settings_app.decorators import allowed_users
from django.db.models import Q
from django.contrib.auth.models import Group, User
from employee.models import CurEmpDivision, CurEmpPosition, EmpSpecialize, Employee, FIDNumber, FIDNumber, LIDNumber, IIDNumber, ContactInfo,\
	LocationTL, AddressTL, LocationInter, Photo, FormalEducation, NonFormalEducation, WorkExperience,\
	EmpDependency, EmpLanguage, DriverLicence, EmpSignature
from django.contrib import messages
from datetime import datetime
from leave.models import Leave, LeaveCount, LeavePeriod, LeaveType
from leave.utils import check_period_date, check_period_range
import pandas as pd
from attendance.models import Attendance, AttendanceStatus, Year, Month
from settings_app.utils import f_monthname
from django.urls import reverse
from onboard.models import Onboard, OnboardEmp, OnboardDet
from trip.models import TripEmp
from training.models import TrainingEmp
from perform.models import Eval, EvalDetA, EvalDetB, Evaluator, EvalDate, EvalFinalScore, EvalYear
from django.db.models import Sum
from django.contrib.auth.hashers import check_password
import urllib
import datetime as dt
from attendance.utils import sum_times, calculate_total_hours_week, get_weeks
from settings_app.models import IPGInfo




@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s', 'de', 'deputy'])
def EmployeeList(request):
	objects = Employee.objects.select_related('locationtl','locationinter').order_by('is_new')
	info = IPGInfo.objects.filter(is_active=True).last()
	host_url = request.get_host()
	path = f'{host_url}/media/{info.cop}'
	path = str(path)
	context = {
		'objects': objects, 'path': 'http://'+path,
		'title': 'Lista Funcionariu', 'legend': 'Lista Funcionariu', 
		'title_p': f' <center> <h2>LISTA FUNCIONARIU</h2> </center>'
	}
	return render(request, 'employee/emp_list.html', context)


###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpRawDataN(request):
	group = request.user.groups.all()[0].name
	objects = []
	emps = Employee.objects.filter().all().order_by('employeedivision__dg__id')
	for i in emps:
		fidnum = FIDNumber.objects.filter(employee=i).first()
		objects.append([i,fidnum])
	context = {
		'group': group, 'objects': objects,
		'title': 'Raw Data Funcionariu', 'legend': 'Raw Data Funcionariu'
	}
	return render(request, 'employee3/emp_raw_data.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def EmpDeactiveList(request):
	group = request.user.groups.all()[0].name
	objects = Employee.objects.filter(status_id=2).prefetch_related('contract').all()
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Funsionario Desativu', 'legend': 'Lista Funsionario Desativu'
	}
	return render(request, 'employee/emp_list_deact.html', context)



# done: EMPLOYEE DETAIL
@login_required
# @allowed_users(allowed_roles=['admin','hr','general'])
def EmployeeDetail(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Employee, hashed=hashid)
	fidnum = FIDNumber.objects.filter(employee=objects).first()
	lidnum = LIDNumber.objects.filter(employee=objects).first()
	iidnum = IIDNumber.objects.filter(employee=objects).first()
	contactinfo = ContactInfo.objects.filter(employee=objects).first()
	loctl = LocationTL.objects.filter(employee=objects).first()
	addtl = AddressTL.objects.filter(employee=objects).first()
	locinter = LocationInter.objects.filter(employee=objects).first()
	img = Photo.objects.filter(employee=objects).first()
	driver = DriverLicence.objects.filter(employee=objects).first()
	empcont = Contract.objects.filter(employee=objects, is_active=True).last()
	empsalary = EmpSalary.objects.filter(contract=empcont).last()
	signature = EmpSignature.objects.filter(employee=objects).last()
	emppos = CurEmpPosition.objects.filter(employee=objects).first()
	empdiv = CurEmpDivision.objects.filter(employee=objects).first()
	empdepend = EmpDependency.objects.filter(employee=objects).all()
	formaledu = FormalEducation.objects.filter(employee=objects).last()
	empplacement = EmpPlacement.objects.filter(employee=objects, is_active=True).last()
	nonformaledu = NonFormalEducation.objects.filter(employee=objects).last()
	workexp = WorkExperience.objects.filter(employee=objects).last()
	emplang = EmpLanguage.objects.filter(employee=objects).all()
	empspecs = EmpSpecialize.objects.filter(employee=objects).all()
	context = {
		'group': group, 'hashid': hashid, 'objects': objects, 'fidnum': fidnum, 'lidnum': lidnum, 'iidnum': iidnum,
		'contactinfo': contactinfo, 'loctl':loctl, 'addtl': addtl, 'locinter':locinter, 'img': img,
		'empcont': empcont, 'empsalary': empsalary, 'emppos': emppos, 'empdiv': empdiv,
		'formaledu': formaledu, 'nonformaledu': nonformaledu, 'workexp': workexp,
		'empdepend': empdepend, 'driver': driver, 'emplang': emplang, 'empspecs': empspecs,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu', 'empplacement':empplacement,
		'page': 'basic', 'employee': objects, 'signature':signature
	}
	return render(request, 'employee/emp_detail.html', context)

###DETAIL ONBOARDING
@login_required
# @allowed_users(allowed_roles=['admin','hr'])
def EmployeeOnboardList(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	try:
		onboardemp = get_object_or_404(OnboardEmp, employee__hashed=hashid)
		emp = onboardemp.employee
		img = Photo.objects.get(employee=emp)
		onboards = Onboard.objects.filter(onboardemp=onboardemp).all()
		objects = []
		for i in onboards:
			a = OnboardDet.objects.filter(onboard=i).all()
			objects.append([i,a])
		context = {
			'group': group, 'onboardemp': onboardemp, 'emp': emp, 'objects': objects, 'img': img, 
			'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu',
			'page': 'onboarding', 'employee':emp
		}
		return render(request, 'employee/emp_detail.html', context)
	except:
		context = { 
			'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu',
			'message': f'Deskulpa, Onboarding ba <strong> {employee} </strong> refere seidauk kria!', 
			'page': 'error', 'employee':employee
		}
		return render(request, 'employee/emp_detail.html', context)

@login_required
def EmployeeLeaveDetail(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	try:
		today = datetime.today().date()
		period = LeavePeriod.objects.filter(employee=employee, is_active=True).last()
		if period:
			period  = get_object_or_404(LeavePeriod, employee=employee, is_active=True)
			leave = Leave.objects.filter(employee=employee, leave_period=period).order_by('-start_date')
			
			min_month = f'{period.start_year.year}-{period.start_month.code}-{period.start_date.day}'
			max_month = f'{today.year}-{today.month}-{period.start_date.day}'
			months = pd.date_range(min_month, max_month, freq='M')
			check_last_period = LeavePeriod.objects.filter(employee=employee,pk__lt=period.pk).last()
			all_period = LeavePeriod.objects.filter(employee=employee)
			last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
			lt = LeaveType.objects.all()
			data = []
			data2 = []
			allmonth = check_period_range(period)
			for obj in allmonth:
				al = LeaveCount.objects.filter(employee=employee, period=period,  month__code=obj.month, year__year=obj.year, leave_type_id=1).last()
				sl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=2).last()
				spl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=3).last()
				mtl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=4).last()
				ptl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=5).last()
				cl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=6).last()
				lmonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=obj.month, start_date__year=obj.year,leave_type_id=1).exists()

				data2.append([obj, al,sl, spl, mtl, ptl, cl, lmonth])
			objects = []
			alleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1).last()
			alleavelast = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__lt=today).last()
			alleavenext = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__gt=today).first()
			sickleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=2).all().order_by('pk')
			spleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=3).all().order_by('pk')
			mtleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=4).all().order_by('pk')
			ptleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=5).all().order_by('pk')
			chleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=6).all().order_by('pk')
			leavecheck = LeaveCount.objects.filter(employee=employee, period=period, period__employee=employee ).exists()
			leavemonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=today.month, start_date__year=today.year,leave_type_id=1).exists()
			objects.append([alleave, spleave,sickleave, mtleave, ptleave,chleave, data, leavemonth, alleavelast,alleavenext])

			check_date = check_period_date(period.start_date)
			check_last_month_per = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1,  month__code=1, year__year=2023).exists()

			context = {
				'group': group, 'employee':employee, 'alleave':alleave, 'period':period, 'leave':leave, 'last_count_period':last_count_period, 'today':check_date,
				'title': 'Balansu Licensa no Historia', 'legend': 'Balansu Licensa no Historia', 'objects': objects, 'leavecheck':leavecheck, 'all_period':all_period, 'contract':contract, \
				'check_last_month_per':check_last_month_per, 'today':today,'allmonth':allmonth, 'data':data2, 'today':today, 'page':'leave'
			}
			return render(request, 'employee/emp_detail.html', context)	
		else:
			messages.error(request, 'Periode Licensa Seidauk Iha!!')
			return redirect('emp-detail', employee.hashed)
	except:
		if contract:
			context = {
				'legend': 'Balansu Licensa no Historia', 'title': 'Balansu Licensa no Historia', 'employee':employee, 'contract': contract, 'page':'leave'
			}
			return render(request, 'employee/emp_detail.html', context)				
		else:
			messages.error(request, 'Contrato seidauk kria!!')
			return redirect('leave-hr-app-raw-list')


@login_required
# @allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def EmployeeAttendanceDetail(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	data_for_weeks = []
	unit = ""
	if empdiv.unit:
		unit = empdiv.unit
	elif empdiv.department:
		unit = empdiv.department.unit
	att_status = AttendanceStatus.objects.all()
	att_objs = []
	tot_hours_all, tot_hours_year, tot_hours_mont, tot_hours_week  = [], [], [], []
	total_hours_all, total_hours_year, total_hours_month, total_hours_week = 0.00,0.00,0.00,0.00
	att = Attendance.objects.filter(employee=emp).all()
	for obj in att:
		time_am, time_pm, time_string_am,time_string_pm = '00:00', '00:00','00:00', '00:00'
		if obj.totat_am:
			time_am = obj.totat_am
			time_string_am = time_am.strftime("%H:%M")
			tot_hours_all.append(time_string_am)
		if obj.totat_pm:
			time_pm = obj.totat_pm
			time_string_pm = time_pm.strftime("%H:%M")
			tot_hours_all.append(time_string_pm)
	tot_hours = sum_times(tot_hours_all)
	total_hours_all = tot_hours

	for i in att_status:
		a = Attendance.objects.filter(employee=emp, status_am=i, status_pm=i).all().count()
		b = Attendance.objects.filter(employee=emp, status_am=i, status_pm__isnull=True).all().count()
		c = Attendance.objects.filter(employee=emp, status_pm=i, status_am__isnull=True).all().count()
		b =  float(0.5 * b )
		c = float(0.5 * c)
		tot = a + b + c
		att_objs.append([i,tot])
	years = Year.objects.filter().all()
	months = Month.objects.filter().all()
	today = dt.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')
	year, month = 0,0
	if request.method == 'POST':
		if request.POST.get("tinan") == "0":
			year = year_now
		else:
			year = request.POST.get("tinan")
		if request.POST.get("fulan") == "0":
			month = month_now
		else:
			month = request.POST.get("fulan")
	att_objs_y,att_objs_m = [],[]


	if not year == 0: 
		att_year = Attendance.objects.filter(employee=emp, date__year=year).all()
		time_yam, time_ypm, time_string_yam,time_string_ypm = '00:00', '00:00','00:00', '00:00'
		for obj2 in att_year:
			if obj2.totat_am:
				time_yam = obj2.totat_am
				time_string_yam = time_yam.strftime("%H:%M")
				tot_hours_year.append(time_string_yam)
			if obj2.totat_pm:
				time_ypm = obj2.totat_pm
				time_string_ypm = time_ypm.strftime("%H:%M")
				tot_hours_year.append(time_string_ypm)
		tot_hours = sum_times(tot_hours_year)
		total_hours_year = tot_hours

	for i in att_status:
		a = 0
		if not year == 0: 
			a = Attendance.objects.filter(employee=emp, status_am=i, status_pm=i,date__year=year).all().count()
			b = Attendance.objects.filter(employee=emp, status_am=i, status_pm__isnull=True,date__year=year).all().count()
			c = Attendance.objects.filter(employee=emp, status_pm=i, status_am__isnull=True,date__year=year).all().count()
			b =  float(0.5 * b )
			c = float(0.5 * c)
			tot = a + b + c
		att_objs_y.append([i,tot])


	if not month == 0: 
		att_month = Attendance.objects.filter(employee=emp, date__year=year, date__month=month).all()
		time_mam, time_mpm, time_string_mam,time_string_mpm = '00:00', '00:00','00:00', '00:00'
		for obj3 in att_month:
			if obj3.totat_am:
				time_mam = obj3.totat_am
				time_string_mam = time_mam.strftime("%H:%M")
				tot_hours_mont.append(time_string_mam)
			if obj3.totat_pm:
				time_mpm = obj3.totat_pm
				time_string_mpm = time_mpm.strftime("%H:%M")
				tot_hours_mont.append(time_string_mpm)
		tot_hours = sum_times(tot_hours_mont)
		total_hours_month = tot_hours
	for j in att_status:
		tot3 = 0
		if not month == 0: 
			a1 = Attendance.objects.filter(employee=emp, status_am=j, status_pm=j, date__year=year, date__month=month).all().count()
			a2 = Attendance.objects.filter(employee=emp, status_am=j, status_pm__isnull=True,date__year=year, date__month=month).all().count()
			a3 = Attendance.objects.filter(employee=emp, status_pm=j, status_am__isnull=True,date__year=year, date__month=month).all().count()
			a2 =  float(0.5 * a2 )
			a3 =  float(0.5 * a3)
			tot3 = a1 + a2 + a3 

		att_objs_m.append([j,tot3])
	if  month != 0 :
		weeks = get_weeks(int(year), int(month))
		cweek = []
		for week in weeks:
			cweek.append([week[0],week[1]])
			att_week = Attendance.objects.filter(employee=emp, date__year=year, date__gte=week[0], date__lte=week[1]).all()
			time_wam, time_wpm, time_string_wam,time_string_wpm = '00:00', '00:00','00:00', '00:00'
			for obj4 in att_week:
				if obj4.totat_am:
					time_wam = obj4.totat_am
					time_string_wam = time_wam.strftime("%H:%M")
				tot_hours_week.append(time_string_wam)
				if obj4.totat_pm:
					time_wpm = obj4.totat_pm
					time_string_wpm = time_wpm.strftime("%H:%M")
				tot_hours_week.append(time_string_wpm)
			thweek = calculate_total_hours_week(week, att_week)
			stime = sum_times(thweek)
			data_for_weeks.append([week[0], week[1], stime])

	monthname = 0
	if not month == 0:
		monthname = f_monthname(int(month))
	context = {
		'group': group, 'unit': unit, 'emp': emp, 'att_objs': att_objs, 'att_objs_y': att_objs_y, 'att_objs_m': att_objs_m,
		'years': years, 'months': months, 'year': year, 'month': month, 'monthname': monthname, 
		'page': 'attendance', 'employee':emp,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu', 
		'total_hours_all':total_hours_all, 'total_hours_year':total_hours_year, 'total_hours_month':total_hours_month, 
		'data_for_weeks':data_for_weeks
	}
	return render(request, 'employee/emp_detail.html', context)


@login_required
def EmployeeTripList(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=employee)
	unit = ""
	if empdiv.unit:
		unit = empdiv.unit
	elif empdiv.department:
		unit = empdiv.department.unit
	emptrip = TripEmp.objects.filter(employee=employee)
	context = {
		'group': group, 'unit': unit,  'page':'trip', 'emp':employee,
		'employee':employee, 'objects':emptrip,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu'
	}
	return render(request, 'employee/emp_detail.html', context)

@login_required
def EmployeeTrainingList(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=employee)
	unit = ""
	if empdiv.unit:
		unit = empdiv.unit
	elif empdiv.department:
		unit = empdiv.department.unit
	emptraining = TrainingEmp.objects.filter(employee=employee)
	context = {
		'group': group, 'unit': unit,  'page':'training', 'emp':employee,
		'employee':employee, 'objects':emptraining,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu'
	}
	return render(request, 'employee/emp_detail.html', context)


@login_required
# @allowed_users(allowed_roles=['unit','hr'])
def EmployeePerformDetail(request, hashid):
	group = request.user.groups.all()[0].name
	today = datetime.today().year
	employee = get_object_or_404(Employee, hashed=hashid)
	c_emp, unit, dep = "","",""
	eval = Eval.objects.filter(employee=employee, year__year=today).last()
	zuri = Evaluator.objects.filter(eval=eval).first()
	evaldate = EvalDate.objects.filter(eval=eval).first()
	finalscore = EvalFinalScore.objects.filter(eval=eval).first()
	obj_as = EvalDetA.objects.filter(eval=eval).all()
	obj_bs = EvalDetB.objects.filter(eval=eval).all()
	sum_a = EvalDetA.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	sum_b = EvalDetB.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	all_year = EvalYear.objects.exclude(year=today)
	context = {
		'group': group, 'c_emp': c_emp, 'unit': unit, 'dep': dep, 'eval': eval, 'zuri': zuri,
		'evaldate': evaldate, 'finalscore': finalscore, 'employee': employee, 'page':'perform',
		'obj_as': obj_as, 'obj_bs': obj_bs, 'sum_a': sum_a, 'sum_b': sum_b,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun', 'all_year':all_year
	}
	return render(request, 'employee/emp_detail.html', context)
@login_required
# @allowed_users(allowed_roles=['unit','hr'])
def EmployeePerformDetailYear(request, hashid, year):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	c_emp, unit, dep = "","",""
	eval = Eval.objects.filter(employee=employee, year__year=year).last()
	zuri = Evaluator.objects.filter(eval=eval).first()
	evaldate = EvalDate.objects.filter(eval=eval).first()
	finalscore = EvalFinalScore.objects.filter(eval=eval).first()
	obj_as = EvalDetA.objects.filter(eval=eval).all()
	obj_bs = EvalDetB.objects.filter(eval=eval).all()
	sum_a = EvalDetA.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	sum_b = EvalDetB.objects.filter(eval=eval).aggregate(Sum('choice__score')).get('choice__score__sum', 0.00)
	all_year = EvalYear.objects.exclude(year=year)
	context = {
		'group': group, 'c_emp': c_emp, 'unit': unit, 'dep': dep, 'eval': eval, 'zuri': zuri,
		'evaldate': evaldate, 'finalscore': finalscore, 'employee': employee, 'page':'perform',
		'obj_as': obj_as, 'obj_bs': obj_bs, 'sum_a': sum_a, 'sum_b': sum_b,
		'title': f'Detalha Avaliasaun', 'legend': f'Detalha Avaliasaun', 'all_year':all_year
	}
	return render(request, 'employee/emp_detail.html', context)


def PasswordValidationView(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	empSalary = EmpSalary.objects.filter(employee=emp, is_active=True).last()
	if request.method == 'POST':
		entered_password = request.POST.get('password')
		user = User.objects.get(pk=request.user.pk)
		if check_password(entered_password, user.password):
			data = 'pass'
			request.session['data'] = data
			return redirect('salary-detail', hashid=empSalary.hashed) 
		else:
			messages.error(request, 'Password Sala!!')
			return redirect('emp-detail', emp.hashed)
	context = {
		'title': 'Validasaun Password','legend':'Valida Ita nia Password', 'emp': emp
	}
	return render(request, 'components/password_validation.html', context)


@login_required
def GoogleMaps(request):
	group = request.user.groups.all()[0].name
	objects = AddressTL.objects.filter(employee__status_id=1,latitude__isnull=False).all()
	context = {
		'group': group, 'objects': objects,
		'title': 'Mapa Hela Fatin Funsionariu', 'legend': 'Mapa Hela Fatin Funsionariu'
	}
	return render(request, 'employee/maps.html', context)


@login_required
def EmployeeContactList(request):
	employee = ContactInfo.objects.filter(employee__status_id=1).distinct()
	context = {
		'title': 'Lista Kontakto Geral','legend':'Lista Kontakto Geral', 'employee': employee
	}
	return render(request, 'employee/emp_contact_list.html', context)