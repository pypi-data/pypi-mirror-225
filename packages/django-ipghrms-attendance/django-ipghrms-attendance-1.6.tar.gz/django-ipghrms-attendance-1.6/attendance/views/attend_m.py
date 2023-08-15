import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from custom.models import Unit
from employee.models import Employee
from contract.models import Contract
from leave.models import Leave
from attendance.models import Attendance, AttendanceTotal, AttendanceUnit, AttendanceStatus, Holiday, Month, Year
from attendance.forms import AttendanceAMForm, AttendancePMForm, AttendanceEmpForm, AttendanceUnitForm
from settings_app.utils import getnewid, f_monthname_eng, f_monthname, number_of_days_in_month
import csv, io, datetime
from settings_app.user_utils import c_unit
from datetime import datetime as dt
from django.utils import timezone
from collections import defaultdict
import pprint
import numpy as np
import pandas as pd
from datetime import date


@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUnitDayEmp(request, pk, day):
	unit = get_object_or_404(Unit, pk=pk)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	year = year.year
	today = str(year)+'-'+str(month.id)+'-'+day
	att_unit = AttendanceUnit.objects.filter(unit=unit, year=year, month=month.id).first()
	emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit))\
		,status_id=1).prefetch_related('curempdivision','curempposition').all().order_by('curempposition__position')
	count = emp.count()
	status = AttendanceStatus.objects.all()
	if request.method == 'POST':
		for i in range(count):
			empid = request.POST.get('empid'+str(i+1))
			amid = request.POST.get('amid'+str(i+1))
			pmid = request.POST.get('pmid'+str(i+1))
			desc = request.POST.get('descid'+str(i+1))
			status_am, status_pm = None, None
			if amid: status_am = AttendanceStatus.objects.filter(pk=amid).first()
			if pmid: status_pm = AttendanceStatus.objects.filter(pk=pmid).first()
			attdiv = AttendanceUnit.objects.filter(unit=unit, year=year, month=month.id).first()
			atttot = AttendanceTotal.objects.filter(employee_id=empid, year=year, month=month.id).first()
			if not attdiv:
				newid_unit, _ = getnewid(AttendanceUnit)
				obj_div = AttendanceUnit(id=newid_unit, unit=unit, year=year, month=month.id)
				obj_div.save()
			if not atttot:
				newid_tot, _ = getnewid(AttendanceTotal)
				obj_tot = AttendanceTotal(id=newid_tot, employee=empid, year=year, month=month.id)
				obj_tot.save()
			att = Attendance.objects.filter(unit=unit, employee_id=empid, date=today).first()
			newid, new_hashid = getnewid(Attendance)
			if not att:
				obj = Attendance(id=newid, unit=unit, employee_id=empid, status_am=status_am, status_pm=status_pm,\
					date=today, year=year, month=month, desc=desc, datetime=datetime.datetime.now(), user=request.user, hashed=new_hashid)
				obj.save()
				messages.success(request, f'Absensia input ona.')
			else:
				messages.warning(request, f'Data Absensia iha ona.')
		return redirect('attend-unit-list', pk=pk)
	context = {
		'unit': unit, 'year': year, 'month': month, 'day': day, 'emp': emp, 'status': status,
		'att_unit': att_unit,
		'title': 'Absensia iha %s' % (unit.code), 'legend': 'Absensia iha %s' % (unit.code)
	}
	return render(request, 'attendance/unit_day_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendProcessAM(request, hashid):
	objects = get_object_or_404(Attendance, hashed=hashid)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	if request.method == 'POST':
		form = AttendanceAMForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Absensia altera ona.')
			return redirect('attend-unit-list', pk=objects.unit.pk)
	else: form = AttendanceAMForm(instance=objects)
	context = {
		'objects': objects, 'month': month, 'year': year, 'form': form,
		'title': 'Procesa', 'legend': 'Procesa'
	}
	return render(request, 'attendance/form_am-pm.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendProcessPM(request, hashid):
	objects = get_object_or_404(Attendance, hashed=hashid)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	if request.method == 'POST':
		form = AttendancePMForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Absensia altera ona.')
			return redirect('attend-unit-list', pk=objects.unit.pk)
	else: form = AttendancePMForm(instance=objects)
	context = {
		'objects': objects, 'month': month, 'year': year, 'form': form,
		'title': 'Procesa', 'legend': 'Procesa'
	}
	return render(request, 'attendance/form_am-pm.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUnitEmpDay(request, pk, hashid):
	unit = get_object_or_404(Unit, pk=pk)
	emp = get_object_or_404(Employee, hashed=hashid)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	att_unit = AttendanceUnit.objects.filter(unit=unit, year=year.year, month=month.id).first()
	tot_days = number_of_days_in_month(int(year.year), int(month.id))
	days = []
	for i in range(1, tot_days+1):
		check2 = datetime.datetime(year.year, month.id, i)
		weekend = check2.strftime("%a")
		if weekend == "Sat" or weekend == "Sun": w = 1
		else: w = 0
		holiday = Holiday.objects.filter(date__month=month.id, date__day=i).first()
		h = 0
		if holiday:
			hh = holiday.date.strftime("%d")
			if int(hh) == i:
				h = 1
		a = Attendance.objects.filter(unit=unit, employee=emp, date__year=year.year, date__month=month.id, date__day=i).first()
		if a: days.append([i,1,w,h,a])
		else: days.append([i,0,w,h])
	if request.method == 'POST':
		messages.warning(request, f'Data Absensia iha ona.')
		return redirect('attend-unit-list', pk=pk)
	context = {
		'unit': unit, 'year': year, 'month': month, 'emp': emp, 'days': days, 'att_unit': att_unit,
		'title': 'Absensia', 'legend': 'Absensia'
	}
	return render(request, 'attendance/unit_emp_date.html', context)
#
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUnitEmpProcess(request, pk, hashid, day):
	unit = get_object_or_404(Unit, pk=pk)
	emp = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=emp).first()
	leave = Leave.objects.filter(employee=emp, is_active=True).first()
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	today = str(year)+'-'+str(month.id)+'-'+day
	if request.method == 'POST':
		newid, new_hashid = getnewid(Attendance)
		form = AttendanceEmpForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.unit = unit
			instance.employee = emp
			instance.date = today
			instance.year = year
			instance.month = month
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()

			attdiv = AttendanceUnit.objects.filter(unit=unit, year=year, month=month).first()
			atttot = AttendanceTotal.objects.filter(employee=emp, unit=unit, year=year, month=month).first()
			if not attdiv:
				newid_unit, _ = getnewid(AttendanceUnit)
				obj_div = AttendanceUnit(id=newid_unit, unit=unit, year=year, month=month)
				obj_div.save()
			if not atttot:
				newid_tot, _ = getnewid(AttendanceTotal)
				obj_tot = AttendanceTotal(id=newid_tot, employee=emp, unit=unit, year=year, month=month)
				obj_tot.save()

			messages.success(request, f'Absensia altera ona.')
			return redirect('attend-unit-emp', pk=unit.pk,hashid=emp.hashed)
	else: form = AttendanceEmpForm()
	context = {
		'unit': unit, 'emp': emp, 'contract': contract, 'leave': leave,
		'month': month, 'year': year, 'day': day, 'form': form,
		'title': 'Procesa', 'legend': 'Procesa'
	}
	return render(request, 'attendance/form_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUnitEmpUpdate(request, pk, hashid, day, pk2):
	unit = get_object_or_404(Unit, pk=pk)
	emp = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=emp).first()
	leave = Leave.objects.filter(employee=emp, is_active=True).first()
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	today = str(year)+'-'+str(month.id)+'-'+day
	objects = get_object_or_404(Attendance, pk=pk2)
	if request.method == 'POST':
		form = AttendanceEmpForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.totat_am = None
			instance.totat_pm = None
			instance.totat_hour = None
			instance.is_hr_update = True
			instance.save()
			messages.success(request, f'Absensia altera ona.')
			return redirect('attend-unit-emp', pk=unit.pk,hashid=emp.hashed)
	else: form = AttendanceEmpForm(instance=objects)
	context = {
		'unit': unit, 'emp': emp, 'contract': contract, 'leave': leave,
		'month': month, 'year': year, 'day': day, 'form': form,
		'title': 'Procesa', 'legend': 'Procesa'
	}
	return render(request, 'attendance/form_emp.html', context)
#
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendPresYes(request, pk, hashid):
	unit = get_object_or_404(Unit, pk=pk)
	objects = get_object_or_404(Attendance, hashed=hashid)
	objects.is_present = True
	objects.save()
	messages.success(request, f'Presensa.')
	return redirect('attend-unit-list', pk=pk)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendPresNo(request, pk, hashid):
	unit = get_object_or_404(Unit, pk=pk)
	objects = get_object_or_404(Attendance, hashed=hashid)
	objects.is_present = False
	objects.save()
	messages.success(request, f'La Presensa.')
	return redirect('attend-unit-list', pk=pk)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUpload(request, unitid, year, month):
	objects = AttendanceUnit.objects.filter(unit_id=unitid, year=year, month=month).first()
	monthname = f_monthname(int(month))
	if request.method == 'POST':
		form = AttendanceUnitForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'File absensia upload ona.')
			return redirect('attend-unit-list', pk=objects.unit.pk)
	else: form = AttendanceUnitForm(instance=objects)
	context = {
		'objects': objects, 'form': form, 'monthname': monthname,
		'title': 'Upload Absensia', 'legend': 'Upload Absensia'
	}
	return render(request, 'attendance/form_upload.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendConfirm(request, pk):
	objects = get_object_or_404(AttendanceUnit, pk=pk)
	objects.is_confirm = True
	objects.save()
	
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	objs = AttendanceTotal.objects.filter(unit=objects.unit, year=year, month=month).all()
	for i in objs:
		a = Attendance.objects.filter(employee=i.employee, year=year, month=month, is_present=False).all().count()
		i.total = a
		i.save()
	messages.success(request, f'Ita boot halo ona konfirmasuan. Iha fase ida nee, sei bele halo alterasaun hodi klike iha butaun Cancela.')
	return redirect('attend-unit-list', pk=objects.unit.pk)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendCancel(request, pk):
	objects = get_object_or_404(AttendanceUnit, pk=pk)
	objects.is_confirm = False
	objects.save()
	messages.success(request, f'Ita boot halo ona cancelamentu. Sei iha posiblidade hodi halo aterasaun.')
	return redirect('attend-unit-list', pk=objects.unit.pk)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendFinalConfirm(request, pk):
	objects = get_object_or_404(AttendanceUnit, pk=pk)
	objects.is_final = True
	objects.save()
	messages.success(request, f'Ita boot halo ona konfirmasaun ikus no sei labele tan halo cancelamentu.')
	return redirect('attend-unit-list', pk=objects.unit.pk)


def time_to_delat(t):
    """Convert datetime.time object with hour and minute to datetime.timedelta object"""
    dt = datetime.timedelta(hours=t.hour, minutes=t.minute)
    return dt
def trans_form_tostring(dt):
    hours = dt.seconds//3600
    minutes = (dt.seconds//60)%60
    seconds = dt.seconds%60
    return f"{hours}:{minutes}:{seconds}"


@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendImport(request, day, month, year):
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	date1 = f'{year.year}-{month.pk}-{day}'
	date1 = dt.strptime(date1, '%Y-%m-%d')
	date1 = date1.strftime('%Y-%m-%d')
	if request.method == 'POST':
		csv_file = request.FILES['fupload']
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'The uploaded file should be in CSV format.')

		# Convert bytes to string
		csv_data = csv_file.read().decode('utf-8')

		# Use StringIO to create a file-like object
		csv_file_obj = io.StringIO(csv_data)

		data_set = pd.read_csv(csv_file_obj, delimiter=',|;', engine='python')
		df = pd.DataFrame(data_set, columns=['PIN', 'Nama Karyawan', 'Tanggal', 'Jam', 'Mode'])
		df = df.assign(AbsenceIn=df['Mode'] == 'Scan Masuk')
		df = df.assign(AbsenceOut=df['Mode'] == 'Scan Keluar')
		df['time'] = pd.to_datetime(df['Jam']).dt.time
		df['date'] = pd.to_datetime(df['Tanggal']).dt.date
		date2 = df.iloc[-1]['date']
		date2 = date2.strftime('%Y-%m-%d')
		if date1 == date2:
			for obj in df['PIN'].unique():
				objects = Employee.objects.filter(pin=obj).first()
				if objects:
					if objects.pin:
						data = df.loc[(df["PIN"] == objects.pin),
							["PIN","date", "time", "Mode", "AbsenceIn", "AbsenceOut"]
						]
						
						newid, hashedid = getnewid(Attendance)
						time1= None
						time2= None
						time3= None
						time4= None
						status_am = False
						status_pm = False
						tot = data.time.shape[0]
						if tot == 4:
							if data.AbsenceIn.iloc[0] == True:
								time1 = data.time.iloc[0]
								status_am = True

							if data.AbsenceOut.iloc[1] == True:
								time2 = data.time.iloc[1]
								status_am = True
							if data.AbsenceIn.iloc[2] == True:
								time3 = data.time.iloc[2]
								status_pm = True
							if data.AbsenceOut.iloc[3] == True:
								time4 = data.time.iloc[3]
								status_pm = True

							
						if tot == 3:
							if data.AbsenceIn.iloc[0] == True:
								time1 = data.time.iloc[0]
								status_am = True
							if data.AbsenceOut.iloc[1] == True:
								time2 = data.time.iloc[1]
								status_am = True
							if data.AbsenceIn.iloc[2] == True:
								time3 = data.time.iloc[2]
								status_pm = True
							time4 = None
						if tot == 2:
							if data.AbsenceIn.iloc[0] == True:
								if data.time.iloc[0].hour < 12:
									time1 = data.time.iloc[0]
									status_am = True
								elif data.time.iloc[0].hour >= 12:
									time3 = data.time.iloc[0]
									status_pm = True
							if data.AbsenceOut.iloc[1] == True:
								if data.time.iloc[1].hour < 14:
									time2 = data.time.iloc[1]
									status_am = True
								elif data.time.iloc[1].hour > 14:
									time4 = data.time.iloc[1]
									status_pm = True
						if tot == 1:
							if data.AbsenceIn.iloc[0] == True:
								if data.time.iloc[0].hour < 12:
									time1 = data.time.iloc[0]
									status_am = True
								elif data.time.iloc[0].hour >= 12:
									time3 = data.time.iloc[0]
									status_pm = True
						if tot == 0:
							time1 = None
							time2 = None
							time3 = None
							time4 = None
						s_am = None
						s_pm = None
						if status_am:
							s_am = get_object_or_404(AttendanceStatus, pk=1)
						if status_pm:
							s_pm = get_object_or_404(AttendanceStatus, pk=1)

						check_att = Attendance.objects.filter(date=date2, employee=objects).exists()
						if check_att:
							messages.error(request, 'Absensia Prienche tiha ona')
						else:
							created = Attendance.objects.update_or_create(
								id = newid,
								unit = objects.curempdivision.unit,
								employee = objects,
								year = year,
								month = month,
								time_am = time1,
								timeout_am = time2,
								time_pm = time3,
								timeout_pm = time4,
								status_am = s_am,
								status_pm = s_pm,
								date = date2,
								datetime=datetime.datetime.now(),
								user=request.user,
								hashed = hashedid)
							
							messages.success(request, 'Susesu Importa Dados Absensia')
						
		else:
			messages.error(request, f'Data Nebe Itaboot Hili, Lahanesan ho Data iha File Absensia')
		return redirect('attend-day-list', day, month.pk, year.year)
	context = {
		'title': 'Import Absensia', 'legend': 'Import Absensia'
	}
	return render(request, 'attendance/import.html', context)