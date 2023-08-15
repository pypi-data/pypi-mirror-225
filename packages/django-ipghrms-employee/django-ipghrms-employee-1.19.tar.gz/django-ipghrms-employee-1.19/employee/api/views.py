import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee, CurEmpDivision, FormalEducation, LocationTL, Country
from contract.models import EmpPosition
from custom.models import EducationLevel, Unit, Department, Municipality
from settings_app.user_utils import c_unit, c_dep

class APIGender(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		object = list()
		group = request.user.groups.all()[0].name
		gender = ['Male', 'Female']
		
		if group == 'unit':
			_, unit = c_unit(request.user)
			for i in gender:
				emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit))).prefetch_related('curempdivision').all().count()
				object.append({
					'name': i,
					'y': emp
				})
		elif group == 'dep':
			_, dep = c_dep(request.user)
			for i in gender:
				emp = Employee.objects.filter((Q(curempdivision__department=dep)), sex=i, status_id=1).prefetch_related('curempdivision').all().count()
				object.append({
					'name': i,
					'y': emp
				})
		else:
			for i in gender:
				emp = Employee.objects.filter(sex=i,status_id=1).all().count()
				object.append({
					'name': i,
					'y': emp
				})
		data = { 'label':'GENDER BALANCE', 'obj': object }
		return Response(data)

class APIAllStaff(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		objects = 0
		males = 0
		females = 0
		science = 0 
		notscience = 0
		if group == 'unit':
			_, unit = c_unit(request.user)
			objects = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit))).prefetch_related('curempdivision').all().count()
			males = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)), sex="Male").prefetch_related('curempdivision').all().count()
			females = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)), sex="Female").prefetch_related('curempdivision').all().count()
		elif group == 'dep':
			_, dep = c_dep(request.user)
			objects = Employee.objects.filter((Q(curempdivision__department=dep))).prefetch_related('curempdivision').all().count()
			males = Employee.objects.filter((Q(curempdivision__department=dep)), sex="Male").prefetch_related('curempdivision').all().count()
			females = Employee.objects.filter((Q(curempdivision__department=dep)), sex="Female").prefetch_related('curempdivision').all().count()
		else:
			objects = Employee.objects.filter(status_id=1).all().count()
			males = Employee.objects.filter(sex="Male", status_id=1).all().count()
			females = Employee.objects.filter(sex="Female", status_id=1).all().count()
			science = Employee.objects.filter(status_id=1, is_science=True).all().count()
			notscience = Employee.objects.filter(status_id=1, is_science=False).all().count()
		data = { 'label': 'Total Funcionario IPG Timor Leste', 'tot': objects, 'male':males, 'female': females, 'science': science, 'notscience': notscience }
		return Response(data)



class APINivelAca(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		nivel = EducationLevel.objects.all()
		label = list()
		obj = list()
		for i in nivel:
			obj2 = 0
			if group == 'unit':
				_, unit = c_unit(request.user)
				a = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)), status_id=1).prefetch_related('curempdivision').all()
			elif group == 'dep':
				_, dep = c_dep(request.user)
				a = Employee.objects.filter((Q(curempdivision__department=dep)), status_id=1).prefetch_related('curempdivision').all()
			else:
				a = Employee.objects.filter(status_id=1).all()
			for j in a:
				b = FormalEducation.objects.filter(employee=j).last()
				if b:
					if b.education_level == i: 
						obj2 = obj2 + 1
			label.append(i.name)
			obj.append({
				'name': i.name,
				'y': obj2
			})
		data = { 'label': 'DISTRIBUISAUN FUNSIONARIO BASEIA BA NIVEL ACADEMIKO', 'obj': obj,  'label2':label}
		return Response(data)

class APIUnit(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		units = Unit.objects.all()
		label = list()
		obj = list()
		d = list()
		for i in units:
			a = CurEmpDivision.objects.filter((Q(unit=i)|Q(department__unit=i))).all().count()
			label.append(i.code)
			obj.append(a)
			d.append({
				'name': i.name,
				'y': a,
				'drilldown':i.name,
			})
			
		data = { 'label': label, 'obj': obj,  'datas': d }
		return Response(data)

class APIDep(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		deps = []
		if group == 'unit':
			_, unit = c_unit(request.user)
			deps = Department.objects.filter(unit=unit).all()
		else:
			deps = Department.objects.filter().all()
		label = list()
		obj = list()
		for i in deps:
			a = CurEmpDivision.objects.filter(department=i).all().count()
			label.append(i.name)
			obj.append({
				'name': i.name,
                'y': a,
			})
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class uAPIDep(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		_, dep = c_dep(request.user)
		label = dep
		obj = list()
		obj = CurEmpDivision.objects.filter(department=dep).all().count()
		data = { 'label': label, 'obj': obj, }
		return Response(data)
###
class APIMun(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		mun = Municipality.objects.all()
		label = list()
		obj = list()
		data2 = []
		for i in mun:
			if group == 'unit':
				_, unit = c_unit(request.user)
				a = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
					locationtl__municipality=i).all().count()
			elif group == 'dep':
				_, dep = c_dep(request.user)
				a = Employee.objects.filter(curempdivision__department=dep, locationtl__municipality=i).all().count()
			else:
				a = Employee.objects.filter(locationtl__municipality=i).all().count()
			label.append(i.name)
			obj.append(a)
			data2.append([i.name, a])
		data = { 'label': label, 'obj': obj, 'data2':data2 }
		return Response(data)

class APICountry(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		country = Country.objects.all()
		label = list()
		obj = list()
		d = list()
		for i in country:
			if group == 'unit':
				_, unit = c_unit(request.user)
				a = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
					country=i).all().count()
				if a > 0:
					label.append(i.name)
					obj.append(a)
			elif group == 'dep':
				_, dep = c_dep(request.user)
				a = Employee.objects.filter(curempdivision__department=dep, country=i).all().count()
				if a > 0:
					label.append(i.name)
					obj.append(a)
			else:
				a = Employee.objects.filter(country=i).all().count()
				if a > 0:
					label.append(i.name)
					obj.append(a)
				d.append({
					'name': i.name,
					'y': a,
					'drilldown':i.name,
				})
				
		data = { 'label': label, 'obj': obj, 'datas':d }
		return Response(data)

class APIAge(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		title = None
		if group == 'unit':
			_, unit = c_unit(request.user)
			emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit))).prefetch_related('curempdivision').all()
		elif group == 'dep':
			_, dep = c_dep(request.user)
			emp = Employee.objects.filter(curempdivision__department=dep).prefetch_related('curempdivision').all()
		else:
			emp = Employee.objects.filter().all()
		age_int = np.array([[17,25],[26,30],[31,40],[41,50],[51,60],[61,70]])
		label = list()
		obj = list()
		age2 = list()
		for i in range (0,len(age_int)):
			lbl = str(age_int[i,0])+' - '+str(age_int[i,1])
			label.append(lbl)
			if group == 'unit':
				a = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),status_id=1).prefetch_related('curempdivision').all()
				title = f'IPG-TL Staff Divizion  {unit.code} based on Age Range'

			elif group == 'dep':
				a = Employee.objects.filter(curempdivision__department=dep, status_id=1).prefetch_related('curempdivision').all()
				title = f'IPG-TL Staff Team  {dep.code} based on Age Range'
			else:
				a = Employee.objects.filter(status_id=1).prefetch_related('curempdivision').all()
				title = f'IPG-TL Staff based on Age Range'
			aa = 0
			for j in a:
				if j.dob:
					b = int(round((datetime.datetime.today().date() - j.dob).days/365.2425,0))
					if b >= age_int[i,0] and b <= age_int[i,1]:
						aa = aa + 1
			obj.append(aa)

			age2.append(aa)
			obj.append({
				'name': lbl,
				'y': aa,
			})
		data = { 'label': label, 'obj': obj, 'age2': age2, 'title':title }
		return Response(data)