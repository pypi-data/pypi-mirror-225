from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import Unit, DE
from employee.models import Employee
from settings_app.upload_utils import upload_attendace
import hashlib
from datetime import datetime, timedelta
from math import ceil
import pandas as pd
from decimal import Decimal
import time

class Year(models.Model):
	year = models.IntegerField(null=True, blank=True)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class Month(models.Model):
	code = models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=20, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		template = '{0.name} '
		return template.format(self)

class AttendanceStatus(models.Model):
	code = models.CharField(max_length=10, null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self):
		template = '{0.code} -> {0.name}'
		return template.format(self)

class Attendance(models.Model):
	leader = models.ForeignKey(DE, null=True, blank=True, on_delete=models.CASCADE, related_name='attendance', verbose_name="Presidente & Vice-Presidente")
	unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.CASCADE, related_name='attendance', verbose_name="Unidade")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance', verbose_name="Pessoal")
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True,blank=True, related_name='attendance')
	month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True,related_name='attendance')
	status_am = models.ForeignKey(AttendanceStatus, null=True,blank=True, on_delete=models.CASCADE, related_name='attendance_am', verbose_name="Dader")
	status_pm = models.ForeignKey(AttendanceStatus, null=True,blank=True, on_delete=models.CASCADE, related_name='attendance_pm', verbose_name="Loro-Kraik")
	time_am = models.TimeField(null=True, blank=True, verbose_name="Horas tama dader")
	timeout_am = models.TimeField(null=True, blank=True, verbose_name="Horas sai meiudia")
	time_pm = models.TimeField(null=True, blank=True, verbose_name="Horas tama loro-kraik")
	timeout_pm = models.TimeField(null=True, blank=True, verbose_name="Horas sai loro-kraik")
	totat_am = models.TimeField(null=True, blank=True, verbose_name="Total Oras Dader")
	totat_pm = models.TimeField(null=True, blank=True, verbose_name="Total Oras Lokraik")
	totat_hour = models.TimeField(null=True, blank=True, verbose_name="Total Oras")
	is_hr_update = models.BooleanField(default=False,blank=True, null=True)
	is_time_am_change = models.BooleanField(default=False,blank=True, null=True)
	is_time_am_out_change = models.BooleanField(default=False,blank=True, null=True)
	is_time_pm_change = models.BooleanField(default=False,blank=True, null=True)
	is_time_pm_out_change = models.BooleanField(default=False,blank=True, null=True)
	is_active = models.BooleanField(default=True,blank=True, null=True)
	date = models.DateField(null=False, verbose_name="Data",blank=True,)
	desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
	is_present = models.BooleanField(default=True, null=True, blank=True, verbose_name="Presensa")
	datetime = models.DateTimeField(null=True,blank=True,)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True,blank=True)
	def __str__(self):
		template = '{0.employee} {0.date}'
		return template.format(self)
	def save(self, *args, **kwargs):
		if self.pk:  # Only check if the instance has been saved before
			try:
				original = Attendance.objects.get(pk=self.pk)
				if original.time_am != self.time_am:
					self.is_time_am_change = True
				if original.timeout_am != self.timeout_am:
					self.is_time_am_out_change = True
				if original.time_pm != self.time_pm:
					self.is_time_pm_change = True
				if original.timeout_pm != self.timeout_pm:
					self.is_time_pm_out_change = True
			except Attendance.DoesNotExist:
					pass

		if self.time_am and self.timeout_am:
			tt1 = datetime.strptime(str(self.time_am), "%H:%M:%S")
			tt2 = datetime.strptime(str(self.timeout_am), "%H:%M:%S")
			t = (tt2 - tt1)
			tt = str(timedelta(days=0, seconds=t.seconds, microseconds=t.microseconds))
			self.totat_am = datetime.strptime(tt, "%H:%M:%S")

		if self.time_pm and self.timeout_pm:
			tt1 = datetime.strptime(str(self.time_pm), "%H:%M:%S")
			tt2 = datetime.strptime(str(self.timeout_pm), "%H:%M:%S")
			t = (tt2 - tt1)
			tt = str(timedelta(days=0, seconds=t.seconds, microseconds=t.microseconds))
			self.totat_pm = datetime.strptime(tt, "%H:%M:%S")

		if self.totat_am and self.totat_pm:
			start = datetime.strptime(str(self.totat_am),"%Y-%m-%d %H:%M:%S")
			end = datetime.strptime(str(self.totat_pm),"%Y-%m-%d %H:%M:%S")
			dt1 = timedelta(hours= start.hour, minutes=start.minute, seconds=start.second, microseconds=start.microsecond)
			dt2 = timedelta(hours= end.hour,  minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
			tot = dt1 + dt2
			self.totat_hour = str(tot)
		self.hashed = hashlib.md5(str(self.id).encode()).hexdigest()
		return super(Attendance, self).save(*args, **kwargs)

class AttendanceTotal(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendancetotal')
	unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE, related_name='attendancetotal', verbose_name="Unidade")
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True)
	total = models.IntegerField(default=False, null=True, blank=True)
	def __str__(self):
		template = '{0.employee} - {0.month} - {0.total}'
		return template.format(self)

class AttendanceUnit(models.Model):
	unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE, related_name='attendanceunit', verbose_name="Unidade")
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True)
	is_confirm = models.BooleanField(default=False, null=True)
	is_final = models.BooleanField(default=False, null=True)
	file = models.FileField(upload_to=upload_attendace, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload PDF")
	def __str__(self):
		template = '{0.unit.code} - {0.year} - {0.month}'
		return template.format(self)
	
class Holiday(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	date = models.DateField(null=False)
	is_active = models.BooleanField(default=True, null=True)
	def __str__(self):
		template = '{0.date}'
		return template.format(self)
