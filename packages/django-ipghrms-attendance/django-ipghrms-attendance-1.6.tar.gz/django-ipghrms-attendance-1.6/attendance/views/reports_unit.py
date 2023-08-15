import datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from custom.models import Unit
from employee.models import Employee
from contract.models import EmpPlacement, EmpPosition
from attendance.models import Attendance, AttendanceUnit, AttendanceStatus, Month, Year, Holiday
from settings_app.user_utils import c_unit
from settings_app.utils import f_monthname, number_of_days_in_month

@login_required
@allowed_users(allowed_roles=['unit'])
def uRAttUnitDash(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	today = datetime.datetime.now()
	year = today.strftime('%Y')
	month = today.strftime('%m')
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
		'title': 'Relatoriu Lista Presensa', 'legend': 'Relatoriu Lista Presensa'
	}
	return render(request, 'attendance_report/r_unit_dash.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def uRAttUnitEmpSearch(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	today = datetime.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')
	queryset_list = EmpPlacement.objects.filter((Q(unit=unit) | Q(department__unit=unit)),\
		is_active=True).prefetch_related().all().order_by()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
		(Q(employee__first_name__icontains=query)|Q(employee__last_name__icontains=query))).distinct()
	else: queryset_list = EmpPlacement.objects.none()
	context = {
		'group': group, 'unit': unit, 'year': year_now, 'month': month_now, 'objects': queryset_list, 'page': 'unit',
		'title': 'Buka Funcionariu iha %s' % (unit.code), 'legend': 'Buka Funcionariu iha %s' % (unit.code)
	}
	return render(request, 'attendance_report/r_emp_search.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def uRAttUnitEmpDash(request, pk, hashid, page):
	group = request.user.groups.all()[0].name
	unit = get_object_or_404(Unit, pk=pk)
	emp = get_object_or_404(Employee, hashed=hashid)
	att_status = AttendanceStatus.objects.all()
	att_objs = []
	for i in att_status:
		a = Attendance.objects.filter(employee=emp, status_pm=i).all().count()
		att_objs.append([i,a])
	years = Year.objects.filter().all()
	months = Month.objects.filter().all()
	today = datetime.datetime.now()
	year_now = today.strftime('%Y')
	month_now = today.strftime('%m')
	year, month = 0,0
	if request.method == 'POST':
		if request.POST.get("tinan") == "0": year = year_now
		else: year = request.POST.get("tinan")
		if request.POST.get("fulan") == "0": month = month_now
		else: month = request.POST.get("fulan")
	att_objs_y,att_objs_m = [],[]
	for i in att_status:
		a = 0
		if not year == 0: 
			a = Attendance.objects.filter(employee=emp, status_pm=i, date__year=year).all().count()
		att_objs_y.append([i,a])
	for j in att_status:
		b = 0
		if not year == 0: 
			b = Attendance.objects.filter(employee=emp, status_pm=j, date__year=year, date__month=month).all().count()
		att_objs_m.append([j,b])
	monthname = 0
	if not month == 0: monthname = f_monthname(int(month))
	context = {
		'group': group, 'unit': unit, 'emp': emp, 'att_objs': att_objs, 'att_objs_y': att_objs_y, 'att_objs_m': att_objs_m,
		'years': years, 'months': months, 'year': year, 'month': month, 'monthname': monthname, 'page': page,
		'title': 'Relatoriu Absensia husi %s' % (emp), 'legend': 'Relatoriu Absensia husi %s' % (emp)
	}
	return render(request, 'attendance_report/r_emp_dash.html', context)