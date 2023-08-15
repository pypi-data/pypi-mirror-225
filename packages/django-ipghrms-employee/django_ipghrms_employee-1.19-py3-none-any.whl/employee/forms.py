from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from employee.models import EmpSpecialize, Employee, FIDNumber, LIDNumber, IIDNumber, ContactInfo,\
	LocationTL, AddressTL, LocationInter, Photo, FormalEducation, NonFormalEducation, WorkExperience,\
	EmpDependency, DriverLicence, EmpLanguage,EmpSignature, Area
from custom.models import AdministrativePost, Village, Position
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from custom.models import University, EducationLevel
class DateInput(forms.DateInput):
	input_type = 'date'

class EmployeeForm(forms.ModelForm):
	dob = forms.DateField(label="Date of birth", widget=DateInput(), required=True)
	class Meta:
		model = Employee
		fields = ['emp_id', 'pin', 'ext', 'first_name','last_name','sex','pob','dob','marital','country','blood',\
			'father','mother', 'is_science']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['dob'].required = False
		self.fields['emp_id'].label = "IPG ID"
		self.fields['emp_id'].widget.attrs['placeholder'] = 'IPG ID'
		self.fields['emp_id'].required = True
		self.fields['pin'].required = True
		self.fields['ext'].required = True
		self.fields['last_name'].required = True
		self.fields['pin'].label = "PIN"
		self.fields['sex'].label = "Generu"
		self.fields['sex'].required = True
		self.fields['dob'].required = True
		self.fields['pin'].widget.attrs['placeholder'] = 'Finger Print PIN'
		self.fields['ext'].widget.attrs['placeholder'] = 'EXT'
		self.fields['pob'].widget.attrs['placeholder'] = 'Fatin Moris'
		self.fields['father'].widget.attrs['placeholder'] = 'Father Name'
		self.fields['mother'].widget.attrs['placeholder'] = 'Mother Name'
		self.fields['first_name'].widget.attrs['placeholder'] = 'Naran Primeiru'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Apelidu'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('emp_id', css_class='form-group col-md-2 mb-0'),
				Column('pin', css_class='form-group col-md-2 mb-0'),
				Column('ext', css_class='form-group col-md-1 mb-0'),
				Column('first_name', css_class='form-group col-md-3 mb-0'),
				Column('last_name', css_class='form-group col-md-2 mb-0'),
				Column('sex', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('blood', css_class='form-group col-md-2 mb-0'),
				Column('pob', css_class='form-group col-md-2 mb-0'),
				Column('dob', css_class='form-group col-md-2 mb-0'),
				Column('marital', css_class='form-group col-md-3 mb-0'),
				Column('country', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('father', css_class='form-group col-md-5 mb-0'),
				Column('mother', css_class='form-group col-md-5 mb-0'),
				Column('is_science', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class FIDNumberForm(forms.ModelForm):
	class Meta:
		model = FIDNumber
		fields = ['niss','payrol_number','customer_name','bank_account','bank','bank_address','iban','file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('payrol_number', css_class='form-group col-md-4 mb-0'),
				Column('niss', css_class='form-group col-md-4 mb-0'),
				Column('bank_account', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('customer_name', css_class='form-group col-md-4 mb-0'),
				Column('bank', css_class='form-group col-md-4 mb-0'),
				Column('iban', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('bank_address', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LIDNumberForm(forms.ModelForm):
	bi_expiry_date = forms.DateField(widget=DateInput(), required=False)
	passport_expiry_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = LIDNumber
		fields = ['electoral','bi','bi_expiry_date','passport','passport_expiry_date',\
			'cert_rdtl','file_el','file_bi','file_pas','file_cert','file_civil']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('cert_rdtl', css_class='form-group col-md-3 mb-0'),
				Column('file_cert', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('electoral', css_class='form-group col-md-3 mb-0'),
				Column('file_el', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('bi', css_class='form-group col-md-3 mb-0'),
				Column('bi_expiry_date', css_class='form-group col-md-2 mb-0'),
				Column('file_bi', css_class='form-group col-md-7 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('passport', css_class='form-group col-md-3 mb-0'),
				Column('passport_expiry_date', css_class='form-group col-md-2 mb-0'),
				Column('file_pas', css_class='form-group col-md-7 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file_civil', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class IIDNumberForm(forms.ModelForm):
	class Meta:
		model = IIDNumber
		fields = ['passport','passport_expiry_date']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('passport', css_class='form-group col-md-3 mb-0'),
				Column('passport_expiry_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContactInfoForm(forms.ModelForm):
	class Meta:
		model = ContactInfo
		fields = [
			'o_email','p_email','phone1', 'phone2',
			'e_person1', 'e_phone1', 'e_email1', 'e_address1','e_relation1',
			'e_person2', 'e_phone2', 'e_email2', 'e_address2','e_relation2'
		]
	def __init__(self, *args, **kwargs):
		super(ContactInfoForm, self).__init__(*args, **kwargs)

class LocationTLForm(forms.ModelForm):
	class Meta:
		model = LocationTL
		fields = ['municipality','administrativepost','village']

	def __init__(self, *args, **kwargs):
		super(LocationTLForm, self).__init__(*args, **kwargs)
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		
		if 'municipality' in self.data:
			try:
				municipality_id = int(self.data.get('municipality'))
				self.fields['administrativepost'].queryset = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.municipality:
			self.fields['administrativepost'].queryset = self.instance.municipality.administrativepost_set.order_by('-id')

		if 'administrativepost' in self.data:
			try:
				administrativepost_id = int(self.data.get('administrativepost'))
				self.fields['village'].queryset = Village.objects.filter(administrativepost_id=administrativepost_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.administrativepost:
			self.fields['village'].queryset = self.instance.administrativepost.village_set.order_by('name')

class AddressTLForm(forms.ModelForm):
	class Meta:
		model = AddressTL
		fields = ['address','municipality','administrativepost','village','latitude','longitude']
	
	def __init__(self, *args, **kwargs):
		super(AddressTLForm, self).__init__(*args, **kwargs)
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		
		if 'municipality' in self.data:
			try:
				municipality_id = int(self.data.get('municipality'))
				self.fields['administrativepost'].queryset = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.municipality:
			self.fields['administrativepost'].queryset = self.instance.municipality.administrativepost_set.order_by('-id')

		if 'administrativepost' in self.data:
			try:
				administrativepost_id = int(self.data.get('administrativepost'))
				self.fields['village'].queryset = Village.objects.filter(administrativepost_id=administrativepost_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.administrativepost:
			self.fields['village'].queryset = self.instance.administrativepost.village_set.order_by('name')

class LocationInterForm(forms.ModelForm):
	class Meta:
		model = LocationInter
		fields = ['city','address','country']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('address', css_class='form-group col-md-6 mb-0'),
				Column('city', css_class='form-group col-md-3 mb-0'),
				Column('country', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


def validate_image(image):
    # Check file extension
    ext = image.name.split('.')[-1]
    if ext.lower() not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('File type not supported.')

    # Check file size
    file_size = image.size
    if file_size > 1024 * 1024 * 0.5:
        raise ValidationError('File size cannot exceed 0.5 MB.')


class PhotoForm(forms.ModelForm):
	image = forms.FileField(label="Upload Photo", required=True)

	def clean_image(self):
		image = self.cleaned_data.get('image')
		if image:
			if image.size > 1024 * 1024 * 0.5:
				raise forms.ValidationError("File size must be less than 0.5MB")
			if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
				raise forms.ValidationError("Invalid file format. Only JPG, JPEG and PNG are allowed.")
		return image

	class Meta:
		model = Photo
		fields = ['image']

class DriverLicenceForm(forms.ModelForm):
	expiry_date = forms.DateField(widget=DateInput(), required=True)
	class Meta:
		model = DriverLicence
		fields = ['number','type','expiry_date','file']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-4 mb-0'),
				Column('type', css_class='form-group col-md-4 mb-0'),
				Column('expiry_date', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EmpDependForm(forms.ModelForm):
	dob = forms.DateField(label="Date of birth", widget=DateInput(), required=False)
	class Meta:
		model = EmpDependency
		fields = ['name','pob','dob','sex','family_relation','file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('sex', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('pob', css_class='form-group col-md-3 mb-0'),
				Column('dob', css_class='form-group col-md-3 mb-0'),				
				Column('family_relation', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <a class="btn btn-secondary" href="{% url 'depend-list' emp.hashed %}" title="Fila"><i class='fa fa-arrow-circle-left'></i> Fila</a> """),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class FormalEduForm(forms.ModelForm):
	graduation_year = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = FormalEducation
		fields = ['education_level','university','faculty','department','area','file', 'graduation_year', 'is_science']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['graduation_year'].label = 'Data Graduasaun'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('university', css_class='form-group col-md-5 mb-0'),
				Column('education_level', css_class='form-group col-md-3 mb-0'),
				Column('faculty', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('department', css_class='form-group col-md-4 mb-0'),
				Column('area', css_class='form-group col-md-4 mb-0'),
				Column('graduation_year', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('is_science', css_class='form-group col-md-4 mb-0'),
				Column('file', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <a class="btn btn-secondary" href="{% url 'formal-edu-list' emp.hashed %}" title="Fila"><i class='fa fa-arrow-circle-left'></i> Fila</a> """),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class NonFormalEduForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=False)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = NonFormalEducation
		fields = ['title','tutelary_entity','start_date','end_date','hours','file', 'year']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['year'].label = 'Tinan Formasaun'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('title', css_class='form-group col-md-6 mb-0'),
				Column('tutelary_entity', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-3 mb-0'),				
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('hours', css_class='form-group col-md-2 mb-0'),		
				Column('year', css_class='form-group col-md-2 mb-0'),		
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <a class="btn btn-secondary" href="{% url 'nonformal-edu-list' emp.hashed %}" title="Fila"><i class='fa fa-arrow-circle-left'></i> Fila</a> """),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class WorkExpForm(forms.ModelForm):
	start_date = forms.DateField(widget=DateInput(), required=False)
	end_date = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = WorkExperience
		fields = ['institute','department','position','start_date','end_date', 'start_year','end_year']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('institute', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('department', css_class='form-group col-md-5 mb-0'),
				Column('position', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-2 mb-0'),
				Column('end_date', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_year', css_class='form-group col-md-6 mb-0'),
				Column('end_year', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <a class="btn btn-secondary" href="{% url 'work-exp-list' emp.hashed %}" title="Fila"><i class='fa fa-arrow-circle-left'></i> Fila</a> """),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class EmpLangForm(forms.ModelForm):
	class Meta:
		model = EmpLanguage
		fields = ['language','speak','read','write', 'file_language']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('language', css_class='form-group col-md-3 mb-0'),
				Column('speak', css_class='form-group col-md-3 mb-0'),
				Column('read', css_class='form-group col-md-3 mb-0'),
				Column('write', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file_language', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class EmpSpecialForm(forms.ModelForm):
	class Meta:
		model = EmpSpecialize
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group col-md-6 mb-0'),
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class='fa fa-save'></i></button> """)
		)
###
class EmpStatusForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = ['status']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('status', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)


class EmpSignatureForm(forms.ModelForm):
	class Meta:
		model = EmpSignature
		fields = ['image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['image'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('image', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EmpCusUniForm(forms.ModelForm):
	class Meta:
		model = University
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['name'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EmpCusAreaForm(forms.ModelForm):
	class Meta:
		model = Area
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['name'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class EmpCusEduLevelForm(forms.ModelForm):
	class Meta:
		model = EducationLevel
		fields = ['name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['name'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
class PasswordForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput)