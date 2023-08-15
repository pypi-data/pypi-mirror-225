import datetime
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from custom.models import Unit
from employee.models import Employee
from attendance.models import Attendance, AttendanceUnit,  Holiday, Month, Year
from settings_app.utils import getnewid, f_monthname_eng, f_monthname, number_of_days_in_month

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendDash(request):
	group = request.user.groups.all()[0].name
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	m = np.linspace(start = 1, stop = 12, num = 12)
	months = []
	for j in m: months.append(f_monthname_eng(int(j)))
	units = Unit.objects.all().order_by('id')
	context = {
		'group': group, 'month': month, 'months': months, 'year': year, 'units': units,
		'title': 'Painel Absensia', 'legend': 'Painel Absensia'
	}
	return render(request, 'attendance/dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendUnitList(request, pk):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=pk)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	att_unit = AttendanceUnit.objects.filter(unit=unit, year=year, month=month).first()
	tot_days = number_of_days_in_month(int(year.year), int(month.id))
	
	days = []
	for i in range(1, tot_days+1):
		check1 = datetime.datetime(year.year, month.id, i)
		weekend = check1.strftime("%a")
		a = Attendance.objects.filter(unit=unit, year=year, month=month, date__day=i).first()
		if weekend == "Sat" or weekend == "Sun": w = 1
		else: w = 0		
		holiday = Holiday.objects.filter(date__month=month.id, date__day=i).first()
		h = 0
		if holiday: 
			hh = holiday.date.strftime("%d")
			if int(hh) == i: h = 1
		if a: days.append([i,1,w,h])
		else: days.append([i,0,w,h])
	emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
		status_id=1)\
		.prefetch_related('curempdivision','curempposition').all()
	objects = []
	for j in emp:
		objects2 = []
		for jj in range(1, tot_days+1):
			check2 = datetime.datetime(year.year, month.id, jj)
			weekend = check2.strftime("%a")
			if weekend == "Sat" or weekend == "Sun": w = 1
			else: w = 0
			holiday = Holiday.objects.filter(date__month=month.id, date__day=jj).first()
			h = 0
			if holiday:
				hh = holiday.date.strftime("%d")
				if int(hh) == jj: h = 1
			a = Attendance.objects.filter(unit=unit, employee=j, year=year, month=month, date__day=jj).last()
			att,status_am,status_pm,ispresent,time_in_am,time_out_am,time_in_pm,time_out_pm,tot_timeam,tot_timepm,tot_time = [],[],[], [],[],[],[],[],[],[],False
			if a:
				att = a.hashed
				status_am = a.status_am
				status_pm = a.status_pm
				time_in_am = a.time_am
				time_out_am = a.timeout_am
				time_in_pm = a.time_pm
				time_out_pm = a.timeout_pm
				tot_timeam = a.totat_am
				tot_timepm = a.totat_pm
				tot_time = a.totat_hour
				ispresent = a.is_present
			objects2.append([att,status_am,status_pm,w,h,ispresent,time_in_am,time_out_am,time_in_pm,time_out_pm, tot_timeam, tot_timepm,tot_time,a])
		objects.append([j,objects2])
	context = {
		'group': group, 'unit': unit, 'att_unit': att_unit, 'month': month, 'year': year, 'days': days, 'emp': emp, 'objects': objects,
		'title': 'Absensia iha %s' % (unit.code), 'legend': 'Absensia iha %s' % (unit.code)
	}
	return render(request, 'attendance/unit_list.html', context)


###
from django.conf import settings
from django.http import FileResponse, Http404
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendPDF(request, pk):
	objects = get_object_or_404(AttendanceUnit, pk=pk)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	# file = objects.file.url
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError:
		raise Http404('not found')


@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendList(request):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=1)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	tot_days = number_of_days_in_month(int(year.year), int(month.id))
	days = []
	for i in range(1, tot_days+1):
		check1 = datetime.datetime(year.year, month.id, i)
		weekend = check1.strftime("%a")
		a = Attendance.objects.filter(year=year, month=month, date__day=i).first()
		b = Attendance.objects.filter(year=year, month=month, date__day=i).exists()
		if weekend == "Sat" or weekend == "Sun": w = 1
		else: w = 0		
		holiday = Holiday.objects.filter(date__month=month.id, date__day=i).first()
		h = 0
		if holiday: 
			hh = holiday.date.strftime("%d")
			if int(hh) == i: h = 1
		if a: days.append([i,1,w,h,b])
		else: days.append([i,0,w,h])
	emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
		status_id=1).exclude()\
		.prefetch_related('curempdivision','curempposition').all().order_by('curempposition__position')
	context = {
		'group': group,  'month': month, 'year': year, 'days': days, 'emp': emp,
		'title': 'Absensia fulan %s' % (month), 'legend': 'Absensia fulan %s' % (month)
	}
	return render(request, 'attendance/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def AttendDayList(request, day, month, year):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=1)
	year = Year.objects.filter(is_active=True).first()
	month = Month.objects.filter(is_active=True).first()
	tot_days = number_of_days_in_month(int(year.year), int(month.id))
	attend = Attendance.objects.filter(date__day=day, date__month=month.pk, date__year=year.year)
	days = []
	for i in range(1, tot_days+1):
		check1 = datetime.datetime(year.year, month.id, i)
		weekend = check1.strftime("%a")
		a = Attendance.objects.filter(unit=unit, year=year, month=month, date__day=i).first()
		if weekend == "Sat" or weekend == "Sun": w = 1
		else: w = 0		
		holiday = Holiday.objects.filter(date__month=month.id, date__day=i).first()
		h = 0
		if holiday: 
			hh = holiday.date.strftime("%d")
			if int(hh) == i: h = 1
		if a: days.append([i,1,w,h])
		else: days.append([i,0,w,h])
	emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
		status_id=1).exclude()\
		.prefetch_related('curempdivision','curempposition').all().order_by('curempposition__position')

	context = {
		'group': group,  'month': month, 'year': year, 'days': days, 'emp': emp,
		'title': f'Absensia iha loron {day} fulan {month} tinan {year}', 'legend': f'Absensia iha loron {day} fulan {month} tinan {year}', 
		'attend':attend, 'day':day
	}
	return render(request, 'attendance/day_list.html', context)