import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Q
from contract.models import EmpPlacement
from custom.models import Unit
from employee.models import Employee, CurEmpDivision
from attendance.models import Attendance, AttendanceUnit, AttendanceStatus, Month, Year, Holiday
from settings_app.utils import f_monthname, number_of_days_in_month
from datetime import time, timedelta, datetime as dtm
import datetime as dt
import calendar
from django.utils import timezone
from attendance.utils import calculate_total_hours_week, sum_times, get_weeks





@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RAttDash(request):
	group = request.user.groups.all()[0].name
	today = datetime.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')
	units = Unit.objects.all().order_by('id')
	context = {
		'group': group, 'units': units, 'year_now': year_now, 'month_now': month_now,
		'title': 'Relatoriu Lista Presensa tuir Divizaun', 'legend': 'Relatoriu Lista Presensa tuir Divizaun'
	}
	return render(request, 'attendance_report/r_dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RAttUnitList(request, pk, year, month):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=pk)
	if request.method == 'POST':
		if request.POST.get("tinan") == "0": year = year
		else: year = request.POST.get("tinan")
		if request.POST.get("fulan") == "0": month = month
		else: month = request.POST.get("fulan")
	year = Year.objects.filter(year=year).first()	
	month = Month.objects.filter(id=month).first()
	years = Year.objects.filter().all()
	months = Month.objects.filter().all()
	att_unit = AttendanceUnit.objects.filter(unit=unit, year=year.year, month=month.id).first()
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
		'group': group, 'unit': unit, 'att_unit': att_unit, 'month': month, 'year': year, 'days': days,
		'emp': emp, 'objects': objects, 'years': years, 'months': months,
		'title': 'Relatoriu Lista Presensa Divizaun', 'legend': 'Relatoriu Lista Presensa Divizaun'
	}
	return render(request, 'attendance_report/r_unit_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RAttEmpSearch(request, pk):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=pk)
	today = datetime.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')

	queryset_list = EmpPlacement.objects.filter(is_active=True).prefetch_related()\
		.all().order_by()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
		(Q(employee__first_name__icontains=query)|Q(employee__last_name__icontains=query))).distinct()
	else:
		queryset_list = EmpPlacement.objects.none()
	context = {
		'group': group, 'unit': unit, 'year': year_now, 'month': month_now, 'objects': queryset_list,
		'title': 'Buka Funcionariu iha %s' % (unit), 'legend': 'Buka Funcionariu iha %s' % (unit)
	}
	return render(request, 'attendance_report/r_emp_search.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RAttEmpSearch(request):
	group = request.user.groups.all()[0].name
	today = datetime.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')
	queryset_list = CurEmpDivision.objects.filter().prefetch_related()\
		.all().order_by()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
		(Q(employee__first_name__icontains=query)|Q(employee__last_name__icontains=query))).distinct()
	else: queryset_list = CurEmpDivision.objects.none()
	context = {
		'group': group, 'year': year_now, 'month': month_now, 'objects': queryset_list,
		'title': 'Relatorio Lista Presensa tuir Funsionariu', 'legend': 'Relatorio Lista Presensa tuir Funsionariu'
	}
	return render(request, 'attendance_report/r_emp_search.html', context)






@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RAttEmpDash(request, hashid):
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
	today = datetime.datetime.now()
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
		'title': 'Relatoriu Absensia husi %s' % (emp), 'legend': 'Relatoriu Absensia husi %s' % (emp), 
		'total_hours_all':total_hours_all, 'total_hours_year':total_hours_year, 'total_hours_month':total_hours_month, 
		'data_for_weeks':data_for_weeks
	}
	return render(request, 'attendance_report/r_emp_dash.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def RLicFalYear(request):
	group = request.user.groups.all()[0].name
	years = Year.objects.filter().all()
	context = {
		'group': group, 'years': years,
		'title': 'Relatorio Falta', 'legend': 'Relatorio Falta'
	}
	return render(request, 'attendance_report/r_licfal_year.html', context)
