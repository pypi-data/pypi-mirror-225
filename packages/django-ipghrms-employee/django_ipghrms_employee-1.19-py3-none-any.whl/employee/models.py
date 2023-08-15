import datetime
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import DE, Department, FamilyRelation,  Country, Municipality, AdministrativePost,\
	Position, Unit,	Village, Aldeia, EducationLevel, University, Language, Year
from settings_app.upload_utils import upload_photo, upload_formal, upload_nonformal, upload_id_card,\
	upload_depend, upload_civilstatus,upload_languages, upload_signature
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Status(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Area(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class EmpYear(models.Model):
	year = models.IntegerField(null=True, blank=True)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class Employee(models.Model):
	emp_id = models.CharField(max_length=10, null=True, blank=True, verbose_name="ID.")
	pin = models.IntegerField(null=True, blank=True)
	first_name = models.CharField(max_length=30, null=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	pob = models.CharField(max_length=100, blank=True, null=True, verbose_name="Place of birth")
	dob = models.DateField(null=True, blank=True)
	ext = models.IntegerField(null=True, blank=True)
	sex = models.CharField(choices=[('Male','Male'),('Female','Female')], max_length=6, null=True, blank=True)
	marital = models.CharField(choices=[('Single','Single'),('Married','Married'),('Divorce','Divorce'),('Widow','Widow')], max_length=15, null=True, blank=False, verbose_name="Marital Status")
	blood = models.CharField(choices=[('A','A'),('B','B'),('AB','AB'),('O','O')], max_length=15, null=True, blank=True)
	father = models.CharField(max_length=100, null=True, blank=True)
	mother = models.CharField(max_length=100, null=True, blank=True)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=False)
	is_new = models.BooleanField(default=False, null=True, blank=True)
	is_science = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.first_name} {0.last_name}'
		return template.format(self)
	def age(self):
		if self.dob:
			return int(round((datetime.date.today() - self.dob).days/365.2425,0))
		else:
			return int(0)

class FIDNumber(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='fidnumber')
	niss = models.CharField(max_length=30, null=True, blank=True)
	payrol_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="Nu. Payrol")
	customer_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Naran Iha Konta")
	bank_account = models.CharField(max_length=30, null=True, blank=True, verbose_name="Nu. Konta")
	bank = models.CharField(max_length=30, null=True, blank=True, verbose_name="Banku")
	bank_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Enderesu Banku")
	iban = models.CharField(max_length=30, null=True, blank=True)
	file = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach bank account")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.niss} | {0.payrol_number} - {0.iban}'
		return template.format(self)
	class Meta:
		verbose_name = "Financial"
		verbose_name_plural = "Financials"

class LIDNumber(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='lidnumber')
	electoral = models.CharField(max_length=30, null=True, blank=False, verbose_name="Electoral Number")
	bi = models.CharField(max_length=30, null=True, blank=True)
	bi_expiry_date = models.DateField(null=True, blank=True)
	passport = models.CharField(max_length=15, null=True, blank=True)
	passport_expiry_date = models.DateField(null=True, blank=True)
	cert_rdtl = models.CharField(max_length=30, null=True, blank=True, verbose_name="Certidaun RDTL")
	file_el = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Electoral")
	file_bi = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach BI")
	file_pas = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Passport")
	file_cert = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Certidaun RDTL")
	file_civil = models.FileField(upload_to=upload_civilstatus, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Civil Status")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.electoral}'
		return template.format(self)

class IIDNumber(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='iidnumber')
	passport = models.CharField(max_length=15, null=True, blank=True)
	passport_expiry_date = models.DateField(null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.passport}'
		return template.format(self)

class ContactInfo(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='contactinfo')
	o_email = models.CharField(max_length=50, null=True, blank=True, verbose_name="Official Email")
	p_email = models.CharField(max_length=50, null=True, blank=True, verbose_name="Private Email")
	phone1 = models.IntegerField(null=True, blank=True, verbose_name="Nu. Telefone I")
	phone2 = models.IntegerField(null=True, blank=True, verbose_name="Nu. Telefone II")
	e_person1 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Emergency Call Fullname I")
	e_phone1 = models.IntegerField(null=True, blank=True, verbose_name="Nu. Telefone Emergensia I")
	e_email1 = models.CharField(max_length=50, null=True, blank=True, verbose_name="Emergency Email II")
	e_address1 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Emergency Contact Address I")
	e_relation1 = models.ForeignKey(FamilyRelation, on_delete=models.CASCADE, null=True, blank=True, related_name="erelation1", verbose_name="Relasaun")
	e_person2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Emergency Call Fullname II")
	e_phone2 = models.IntegerField(null=True, blank=True, verbose_name="Nu. Telefone Emergensia II")
	e_email2 = models.CharField(max_length=50, null=True, blank=True, verbose_name="Emergency Email II")
	e_address2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="Emergency Contact Address II")
	e_relation2 = models.ForeignKey(FamilyRelation, on_delete=models.CASCADE, null=True, blank=True, related_name="erelation2", verbose_name="Relasaun")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.o_email}/{0.phone1}'
		return template.format(self)

class LocationTL(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='locationtl')
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True)
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True)
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)
	aldeia = models.CharField(max_length=50, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.municipality}'
		return template.format(self)

class AddressTL(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='addresstl')
	address = models.CharField(max_length=50, null=True, blank=True)
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True)
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True)
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)
	aldeia = models.CharField(max_length=50, null=True, blank=True)
	latitude = models.CharField(max_length=20, null=True, blank=True)
	longitude = models.CharField(max_length=20, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.address}'
		return template.format(self)

class LocationInter(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='locationinter')
	address = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.city}'
		return template.format(self)


class Photo(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='photo')
	image = models.ImageField(default='default.jpg', upload_to=upload_photo, null=True,  blank=True,
	validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ])
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.employee}'
		return template.format(self)

class DriverLicence(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='driverlicence')
	number = models.CharField(max_length=30, null=True, blank=True)
	type = models.CharField(max_length=30, null=True, blank=True)
	expiry_date = models.DateField(max_length=15, null=True, blank=True)
	file = models.FileField(upload_to=upload_id_card, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attachment")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		template = '{0.number}'
		return template.format(self)

class EmpDependency(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="empdependency")
	name = models.CharField(max_length=50, null=True)
	pob = models.CharField(max_length=100, blank=True, null=True, verbose_name="Place of birth")
	dob = models.DateField(null=True, blank=True)
	sex = models.CharField(choices=[('Male','Male'),('Female','Female')], max_length=6, null=True, blank=True)
	family_relation = models.ForeignKey(FamilyRelation, on_delete=models.CASCADE, related_name="empdependency")
	file = models.FileField(upload_to=upload_depend, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attachment")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class FormalEducation(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="formaleducation")
	education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, related_name="formaleducation")
	university = models.ForeignKey(University, null=True, blank=True, on_delete=models.CASCADE, related_name="formaleducation")
	faculty = models.CharField(max_length=100, null=True, blank=True)
	department = models.CharField(max_length=100, null=True, blank=True)
	area =  models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
	graduation_year = models.DateField(null=True, blank=True)
	year = models.ForeignKey(EmpYear, on_delete=models.CASCADE, null=True, blank=True)
	file = models.FileField(upload_to=upload_formal, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach certificate")
	is_active = models.BooleanField(default=True)
	is_science = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.education_level}'
		return template.format(self)

class NonFormalEducation(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="nonformaleducation")
	title = models.CharField(max_length=500, null=True, blank=True)
	tutelary_entity = models.CharField(max_length=100, null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	hours = models.IntegerField(null=True, blank=True)
	area = models.CharField(max_length=200, null=True, blank=True)
	file = models.FileField(upload_to=upload_nonformal, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach certicate")
	is_active = models.BooleanField(default=True)
	traning_id = models.IntegerField(null=True, blank=True)
	year = models.ForeignKey(EmpYear, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.title}'
		return template.format(self)

class WorkExperience(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="workexperience")
	institute = models.CharField(max_length=100, null=True, blank=True)
	department = models.CharField(max_length=200, null=True, blank=True)
	position = models.CharField(max_length=50, null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	start_year = models.ForeignKey(EmpYear, on_delete=models.CASCADE, null=True, blank=True, related_name="start_year")
	end_year = models.ForeignKey(EmpYear, on_delete=models.CASCADE, null=True, blank=True, related_name="end_year")
	is_active = models.BooleanField(default=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.institute}'
		return template.format(self)

class EmpLanguage(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="emplanguage")
	language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name="emplanguage")
	speak = models.CharField(choices=[('Native','Native'),('Good','Good'),('Sufficient','Sufficient'),('Basic','Basic')], max_length=15, null=True, blank=True)
	read = models.CharField(choices=[('Native','Native'),('Good','Good'),('Sufficient','Sufficient'),('Basic','Basic')], max_length=15, null=True, blank=True)
	write = models.CharField(choices=[('Native','Native'),('Good','Good'),('Sufficient','Sufficient'),('Basic','Basic')], max_length=15, null=True, blank=True)
	file_language = models.FileField(upload_to=upload_languages, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Attach Certificado")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} {0.language}'
		return template.format(self)

class EmpSpecialize(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="empspecialize")
	name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Epecialidade")
	def __str__(self):
		template = '{0.employee} {0.name}'
		return template.format(self)


class EmpSignature(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="empsignature")
	image = models.ImageField(default='default.jpg', upload_to=upload_signature, null=True,  blank=True,
	validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ])
	def __str__(self):
		template = '{0.employee}'
		return template.format(self)

class EmployeeUser(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeeuser")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		template = '{0.employee}-{0.user}'
		return template.format(self)

class CurEmpPosition(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, related_name="curempposition")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="curempposition")
	def __str__(self):
		template = '{0.employee.first_name} - {0.position}'
		return template.format(self)

class CurEmpDivision(models.Model):
	employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, related_name="curempdivision")
	de = models.ForeignKey(DE, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Presidente/Vice",  related_name="curempdivision")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, related_name="curempdivision")
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="curempdivision")
	def __str__(self):
		template = '{0.employee.first_name} - {0.de}/{0.unit}/{0.department}'
		return template.format(self)
