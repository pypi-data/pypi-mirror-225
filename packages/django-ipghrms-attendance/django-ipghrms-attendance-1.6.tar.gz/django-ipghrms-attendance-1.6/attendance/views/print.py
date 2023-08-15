import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from custom.models import Unit
from employee.models import Employee, CurEmpDivision, CurEmpPosition, FIDNumber
from contract.models import Contract, EmpPlacement
from contract.models import EmpPosition
from attendance.models import Attendance, AttendanceUnit, AttendanceStatus, Month, Year, Holiday
from settings_app.utils import f_monthname, number_of_days_in_month

@login_required
# @allowed_users(allowed_roles=['hr','admin'])
def AttendPrint(request, pk, year, month):
	unit = get_object_or_404(Unit, pk=pk)
	year = Year.objects.filter(year=year).first()
	month = Month.objects.filter(id=month).first()
	att_unit = AttendanceUnit.objects.filter(unit=unit, year=year.year, month=month.id).first()
	tot_days = number_of_days_in_month(int(year.year), int(month.id))
	days = []
	for i in range(1, tot_days+1):
		check1 = datetime.datetime(year.year, month.id, i)
		weekend = check1.strftime("%a")
		a = Attendance.objects.filter(unit=unit, date__year=year.year, date__month=month.id, date__day=i).first()
		if weekend == "Sat" or weekend == "Sun": w = 1
		else: w = 0		
		holiday = Holiday.objects.filter(date__month=month.id, date__day=i).first()
		h = 0
		if holiday:
			hh = holiday.date.strftime("%d")
			if int(hh) == i:
				h = 1
		if a: days.append([i,1,w,h])
		else: days.append([i,0,w,h])
	emp = Employee.objects.filter((Q(curempdivision__unit=unit)|Q(curempdivision__department__unit=unit)),\
		status_id=1).prefetch_related('curempdivision','curempposition')\
		.all().order_by('curempposition__position')
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
				if int(hh) == jj:
					h = 1
			a = Attendance.objects.filter(unit=unit, employee=j, date__year=year.year, date__month=month.id, date__day=jj).first()
			att,status_am,status_pm = [],[],[]
			if a:
				att = a.hashed
				status_am = a.status_am
				status_pm = a.status_pm
			objects2.append([att,status_am,status_pm,w,h])
		objects.append([j,objects2])
	att_status_1 = AttendanceStatus.objects.filter().all().order_by('id')[0:7]
	att_status_2 = AttendanceStatus.objects.filter().all().order_by('id')[7:14]
	att_status_3 = AttendanceStatus.objects.filter().all().order_by('id')[14:]
	# diretor_rh = EmpPosition.objects.filter(position_id=5, unit_id=1, is_active=True).first()
	diretor_rh = []
	context = {
		'unit': unit, 'att_unit': att_unit, 'month': month, 'year': year, 'days': days, 'emp': emp, 'objects': objects,
		'att_status_1': att_status_1, 'att_status_2': att_status_2, 'att_status_3': att_status_3, 'diretor_rh': diretor_rh,
		'title': 'Absensia iha %s' % (unit.code), 'legend': 'Absensia iha %s' % (unit.code)
	}
	return render(request, 'attendance_print/print_attend.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def PrintRAttEmpGeral(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	unit = ""
	if empdiv.unit: unit = empdiv.unit
	elif empdiv.department: unit = empdiv.department.unit
	att_status = AttendanceStatus.objects.all()
	att_objs = []
	for i in att_status:
		a = Attendance.objects.filter(employee=emp, status_pm=i).all().count()
		att_objs.append([i,a])
	context = {
		'unit': unit, 'emp': emp, 'att_objs': att_objs,		
		'title': 'Relatoriu Absensia Geral', 'legend': 'Relatoriu Absensia Geral'
	}
	return render(request, 'attendance_print/print_r_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def PrintRAttEmpYear(request, hashid, year):
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	unit = ""
	if empdiv.unit: unit = empdiv.unit
	elif empdiv.department: unit = empdiv.department.unit
	att_status = AttendanceStatus.objects.all()
	att_objs = []
	for i in att_status:
		a = 0
		if not year == 0: 
			a = Attendance.objects.filter(employee=emp, status_pm=i, date__year=year).all().count()
		att_objs.append([i,a])
	context = {
		'unit': unit, 'emp': emp, 'att_objs': att_objs, 'year': year,
		'title': 'Relatoriu Absensia Tinan %s' % (year), 'legend': 'Relatoriu Absensia Tinan %s' % (year)
	}
	return render(request, 'attendance_print/print_r_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def PrintRAttEmpMonth(request, hashid, year, month):
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=emp)
	unit = ""
	if empdiv.unit: unit = empdiv.unit
	elif empdiv.department: unit = empdiv.department.unit
	att_status = AttendanceStatus.objects.all()
	att_objs = []
	for j in att_status:
		b = 0
		if not month == 0: 
			b = Attendance.objects.filter(employee=emp, status_pm=j, date__year=year, date__month=month).all().count()
		att_objs.append([j,b])
	monthname = 0
	if not month == 0: monthname = f_monthname(int(month))
	context = {
		'unit': unit, 'emp': emp, 'att_objs': att_objs, 'year': year, 'month': month, 'monthname': monthname,
		'title': 'Relatoriu Absensia Fulan %s Tinan %s' % (monthname,year), 'legend': 'Relatoriu Absensia Fulan %s Tinan %s' % (monthname,year)
	}
	return render(request, 'attendance_print/print_r_emp.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s','de','deputy'])
def PrintLicFal(request, year):
	months = Month.objects.filter().all()
	att_status = AttendanceStatus.objects.exclude(pk=1).all()
	tot_att_status = att_status.count()+1
	emps = Employee.objects.exclude((Q(status_id=2)|Q(status_id=3)|Q(status_id=4)|Q(status_id=3)|Q(status_id=10)))\
		.all().order_by('first_name','last_name')
	objects = []
	for i in emps:
		fidnum = FIDNumber.objects.filter(employee=i).first()
		cont = Contract.objects.filter(employee=i, is_active=True).last()
		empdiv = CurEmpDivision.objects.filter(employee=i).first()
		emppos = CurEmpPosition.objects.filter(employee=i).first()
		objects2 = []
		for j in att_status:
			att = Attendance.objects.filter(employee=i, status_pm=j, date__year=year).distinct().values('status_pm').count()
			att_1 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=1).distinct().values('status_pm').count()
			att_2 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=2).distinct().values('status_pm').count()
			att_3 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=3).distinct().values('status_pm').count()
			att_4 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=4).distinct().values('status_pm').count()
			att_5 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=5).distinct().values('status_pm').count()
			att_6 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=6).distinct().values('status_pm').count()
			att_7 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=7).distinct().values('status_pm').count()
			att_8 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=8).distinct().values('status_pm').count()
			att_9 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=9).distinct().values('status_pm').count()
			att_10 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=10).distinct().values('status_pm').count()
			att_11 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=11).distinct().values('status_pm').count()
			att_12 = Attendance.objects.filter(employee=i, status_pm=j, date__year=year, date__month=12).distinct().values('status_pm').count()
			objects2.append([j.code,att,att_1,att_2,att_3,att_4,att_5,att_6,att_7,att_8,att_9,\
				att_10,att_11,att_12])
		objects.append([i,fidnum,fidnum,cont,empdiv,emppos,objects2])
	context = {
		'year': year, 'months': months, 'att_status': att_status, 'tot_att_status': tot_att_status,
		'objects': objects,
		'title': 'Relatoriu Licenca no Faltas', 'legend': 'Relatoriu Licenca no Faltas'
	}
	return render(request, 'attendance_print/print_r_lic_fal.html', context)