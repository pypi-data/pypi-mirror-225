from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from employee.models import Employee
from attendance.models import Attendance, AttendanceUnit, AttendanceStatus, Holiday

class DateInput(forms.DateInput):
	input_type = 'date'

class TimeInput(forms.TimeInput):
	input_type = 'time'

class DateForm(forms.Form):
	datepicker = forms.DateField(widget=DateInput(), required=True, label="Data")

class AttendanceAMForm(forms.ModelForm):
	status_am = forms.ModelChoiceField(label="Dader", required=True, queryset=AttendanceStatus.objects.all())
	time_am = forms.TimeField(label="Horas dader", widget=TimeInput(), required=False)
	class Meta:
		model = Attendance
		fields = ['status_am','time_am']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('status_am', css_class='form-group col-md-6 mb-0'),
				Column('time_am', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)

class AttendancePMForm(forms.ModelForm):
	status_pm = forms.ModelChoiceField(label="Loro-kraik", required=True, queryset=AttendanceStatus.objects.all())
	time_pm = forms.TimeField(label="Horas loro-kraik", widget=TimeInput(), required=False)
	class Meta:
		model = Attendance
		fields = ['status_pm','time_pm']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('status_pm', css_class='form-group col-md-6 mb-0'),
				Column('time_pm', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)

class AttendanceEmpForm(forms.ModelForm):
	status_am = forms.ModelChoiceField(label="Dader", required=False, queryset=AttendanceStatus.objects.all())
	status_pm = forms.ModelChoiceField(label="Loro-Kraik", required=False, queryset=AttendanceStatus.objects.all())
	time_am = forms.TimeField(label="Horas tama dader", widget=TimeInput(), required=False)
	time_pm = forms.TimeField(label="Horas tama loro-kraik", widget=TimeInput(), required=False)
	timeout_am = forms.TimeField(label="Horas sai dader", widget=TimeInput(), required=False)
	timeout_pm = forms.TimeField(label="Horas sai loro-kraik", widget=TimeInput(), required=False)
	class Meta:
		model = Attendance
		fields = ['status_am','time_am','status_pm','time_pm','desc', 'timeout_am', 'timeout_pm']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('status_am', css_class='form-group col-md-4 mb-0'),
				Column('time_am', css_class='form-group col-md-4 mb-0'),
				Column('timeout_am', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('status_pm', css_class='form-group col-md-4 mb-0'),
				Column('time_pm', css_class='form-group col-md-4 mb-0'),
				Column('timeout_pm', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)

class AttendanceUnitForm(forms.ModelForm):
	class Meta:
		model = AttendanceUnit
		fields = ['file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('file', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)
###
class AttendanceStatusForm(forms.ModelForm):
	class Meta:
		model = AttendanceStatus
		fields = ['code','name']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('code', css_class='form-group col-md-2 mb-0'),
				Column('name', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)

class HolidayForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	class Meta:
		model = Holiday
		fields = ['name','date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['name'].required = True
		self.fields['name'].label = 'Deskrisaun Loron Feriadu'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-8 mb-0'),
				Column('date', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai"> Rai <i class="fa fa-save"></i></button> """)
		)
