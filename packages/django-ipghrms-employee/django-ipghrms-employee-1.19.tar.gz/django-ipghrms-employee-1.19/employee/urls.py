from django.urls import path
from . import views

urlpatterns = [
	path('dash/', views.EmployeeDash, name="emp-dash"),
	path('list/', views.EmployeeList, name="emp-list"),
	path('raw/data/', views.EmpRawData, name="emp-rawdata"),
	path('add/', views.EmployeeAdd, name="emp-add"),
	path('update/<str:hashid>/', views.EmployeeUpdate, name="emp-update"),
	path('fid/update/<str:hashid>/', views.FIDNumberUpdate, name="fidnumber-update"),
	path('lid/update/<str:hashid>/', views.LIDNumberUpdate, name="lidnumber-update"),
	path('iid/update/<str:hashid>/', views.IIDNumberUpdate, name="iidnumber-update"),
	path('contactinfo/update/<str:hashid>/', views.ContactInfoUpdate, name="contactinfo-update"),
	path('loctl/update/<str:hashid>/', views.LocationTLUpdate, name="loctl-update"),
	path('locinter/update/<str:hashid>/', views.LocationInterUpdate, name="locinter-update"),
	path('addresstl/update/<str:hashid>/', views.AddressTLUpdate, name="addtl-update"),
	path('photo/update/<str:hashid>/', views.PhotoUpdate, name="photo-update"),
	path('driverlicence/update/<str:hashid>/', views.DriverLicenceUpdate, name="driver-update"),
	path('status/update/<str:hashid>/', views.StatusUpdate, name="status-update"),
	path('new/<str:hashid>/', views.EmployeeIsNew, name="emp-new"),
	path('old/<str:hashid>/', views.EmployeeIsOld, name="emp-old"),
	path('contact/list/', views.EmployeeContactList, name="emp-contact-list-all"),
	path('signature/add/<str:hashid>/', views.EmployeeAddSignature, name="emp-signature-add"),
	path('signature/update/<str:hashid>/<int:pk>/', views.EmployeeUpdateSignature, name="emp-signature-update"),
		
	path('depend/list/<str:hashid>/', views.EmpDependList, name="depend-list"),
	path('depend/detail/<str:hashid>/<str:hashid2>/', views.EmpDependDetail, name="depend-detail"),
	path('depend/add/<str:hashid>/<str:page>/', views.EmpDependAdd, name="depend-add"),
	path('depend/update/<str:hashid>/<str:hashid2>/<str:page>/', views.EmpDependUpdate, name="depend-update"),
	path('formal/list/<str:hashid>/', views.EmpFormalEduList, name="formal-edu-list"),
	path('formal/detail/<str:hashid>/<str:hashid2>/', views.EmpFormalEduDetail, name="formal-edu-detail"),
	path('formal/add/<str:hashid>/add/<str:page>/', views.EmpFormalEduAdd, name="formal-edu-add"),
	path('formal/update/<str:hashid>/<str:hashid2>/<str:page>/', views.EmpFormalEduUpdate, name="formal-edu-update"),
	path('nonformal/list/<str:hashid>/', views.EmpNonFormalEduList, name="nonformal-edu-list"),
	path('nonformal/detail/<str:hashid>/<str:hashid2>/', views.EmpNonFormalEduDetail, name="nonformal-edu-detail"),
	path('nonformal/add/<str:hashid>/<str:page>/', views.EmpNonFormalEduAdd, name="nonformal-edu-add"),
	path('nonformal/update/<str:hashid>/<str:hashid2>/<str:page>/', views.EmplNonFormalEduUpdate, name="nonformal-edu-update"),
	path('workexp/list/<str:hashid>/', views.EmpWorkExpList, name="work-exp-list"),
	path('workexp/detail/<str:hashid>/<str:hashid2>/', views.EmpWorkExpDetail, name="work-exp-detail"),
	path('workexp/add/<str:hashid>/<str:page>/', views.EmpWorkExpAdd, name="work-exp-add"),
	path('workexp/update/<str:hashid>/<str:hashid2>/<str:page>/', views.EmpWorkExpUpdate, name="work-exp-update"),
	path('lang/<str:hashid>/add/', views.EmpLangAdd, name="emp-lang-add"),
	path('lang/<str:hashid>/<str:hashid2>/update/', views.EmpLangUpdate, name="emp-lang-update"),
	path('spec/<str:hashid>/add/', views.EmpSpecialAdd, name="emp-spec-add"),
	path('spec/<str:hashid>/<int:pk>/delete/', views.EmpSpecialDelete, name="emp-spec-delete"),
	
	# path('certificate/<str:hashid>/<str:page>/', views.Employee2PDF, name="employee-certificate"),

	path('attachments/<str:hashid>/', views.EmployeeAttachment, name="emp-attach"),
	path('all/attachments/<str:hashid>/', views.SEmployeeAttachment, name="s-emp-attach"),
	
	path('lid/pdf/<str:hashid>/<str:page>/', views.EmployeeLIDNumPDF, name="emp-lid-pdf"),

	path('no/division/', views.EmpNoDivList, name="emp-no-div"),
	path('general/maps/', views.GoogleMaps, name="emp-maps"),


	path('dep/list/<str:pk>/', views.EmpDepList, name="emp-dep-list"),
	path('unit/list/<str:pk>/', views.EmpUnitList, name="emp-unit-list"),
	path('unit/staff/list/<str:pk>/', views.EmpUnitStaffList, name="emp-unit-staff-list"),
	path('adv/list/', views.AdvList, name="adv-list"),

	# path('raw/data/', views.EmpRawData, name="emp-raw-data")
	path('advisor/raw/data/', views.AdvisorRawData, name="adv-raw-data"),
	path('habi/raw/data/', views.HabiRawData, name="habi-raw-data"),

	path('chart/dash/', views.EmpChartDash, name="emp-chart-dash"),
	#Unit
	path('u/unit/dash/', views.UEmpUnitDash, name="u-emp-unit-dash"),
	path('u/dep/list/<str:pk>/', views.UEmpDepList, name="u-emp-dep-list"),
	#Dep
	path('u/dep/dash/', views.UEmpDepDash, name="u-emp-dep-dash"),
	path('list/deactive/', views.EmpDeactiveList, name="emp-deactive-list"),

	# DETAIL
	path('detail/<str:hashid>/', views.EmployeeDetail, name="emp-detail"),
	path('detail/<str:hashid>/onboarding/', views.EmployeeOnboardList, name="emp-detail-onboarding"),
	path('detail/<str:hashid>/leave/', views.EmployeeLeaveDetail, name="emp-detail-leave"),
	path('detail/<str:hashid>/attendance/', views.EmployeeAttendanceDetail, name="emp-detail-attendance"),
	path('detail/<str:hashid>/trip/', views.EmployeeTripList, name="emp-detail-trip"),
	path('detail/<str:hashid>/training/', views.EmployeeTrainingList, name="emp-detail-training"),
	path('detail/<str:hashid>/evaluation/', views.EmployeePerformDetail, name="emp-detail-evaluation"),
	path('detail/<str:hashid>/<int:year>/evaluation/', views.EmployeePerformDetailYear, name="emp-detail-year-evaluation"),
	path('password_modal/<str:hashid>/', views.CheckPassword, name='password-check'),
	path('pass/val/view/<str:hashid>/', views.PasswordValidationView, name='password-val-view'),
    
	
	path('custom/university-list/<str:hashid>/', views.EmpCustomUniversityList, name='custom-uni-list'),
	path('custom/university-add/<str:hashid>/', views.EmpCustomUniversityAdd, name='custom-uni-add'),
	path('custom/university-update/<int:pk>/<str:hashid>/', views.EmpCustomUniversityUpdate, name='custom-uni-update'),
    path('custom/area-list/<str:hashid>/', views.EmpCustomAreaList, name='custom-area-list'),
	path('custom/area-add/<str:hashid>/', views.EmpCustomAreaAdd, name='custom-area-add'),
	path('custom/are-update/<int:pk>/<str:hashid>/', views.EmpCustomAreaUpdate, name='custom-area-update'),
    
	path('custom/edulevel-list/<str:hashid>/', views.EmpCustomEduLevelList, name='custom-edu-list'),
	path('custom/edulevel-add/<str:hashid>/', views.EmpCustomEduLevelAdd, name='custom-edu-add'),
	path('custom/edulevel-update/<int:pk>/<str:hashid>/', views.EmpCustomEduLevelUpdate, name='custom-edu-update'),
]