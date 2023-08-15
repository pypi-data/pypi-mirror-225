import datetime
from hashlib import new
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from attendance.models import AttendanceStatus, Month, Year, Holiday
from attendance.forms import AttendanceStatusForm, HolidayForm
from settings_app.utils import getnewid

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AttendanceSetDash(request):
	group = request.user.groups.all()[0].name
	years = Year.objects.all()
	months = Month.objects.all()
	status = AttendanceStatus.objects.all()
	holiday = Holiday.objects.all()
	y_active = Year.objects.filter(is_active=True).first()
	context = {
		'group': group, 'years': years, 'months': months, 'status': status, 'holiday': holiday, 'y_active': y_active,
		'title': 'Konfigurasaun', 'legend': 'Konfigurasaun Absensia'
	}
	return render(request, 'attendance_custom/dash.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AttendanceSetYear(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Year, pk=pk)
	objects2 = Year.objects.exclude(pk=pk).all()
	objects.is_active = True
	objects.save()
	for i in objects2:
		i.is_active = False
		i.save()
	messages.success(request, f'Tinan %s ativa ona.' % (objects))
	return redirect('attend-custom-dash')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AttendanceSetMonth(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Month, pk=pk)
	objects2 = Month.objects.exclude(pk=pk).all()
	objects.is_active = True
	objects.save()
	for i in objects2:
		i.is_active = False
		i.save()
	messages.success(request, f'Fulan %s ativa ona.' % (objects))
	return redirect('attend-custom-dash')

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AttendanceStatusAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid, _ = getnewid(AttendanceStatus)
		form = AttendanceStatusForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.save()
			messages.success(request, f'Status foun amenta ona.')
			return redirect('attend-custom-dash')
	else: form = AttendanceStatusForm()
	context = {
		'group': group, 'form': form,
		'title': 'Aumenta Status Absensia', 'legend': 'Aumenta Status Absensia'
	}
	return render(request, 'attendance_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def AttendanceStatusUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(AttendanceStatus, pk=pk)
	if request.method == 'POST':
		form = AttendanceStatusForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Status aleta ona ona.')
			return redirect('attend-custom-dash')
	else: form = AttendanceStatusForm(instance=objects)
	context = {
		'group': group, 'form': form,
		'title': 'Altera Status Absensia', 'legend': 'Altera Status Absensia'
	}
	return render(request, 'attendance_custom/form.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def HolidayList(request):
	group = request.user.groups.all()[0].name
	objects = Holiday.objects.all()
	context = {
		'group': group, 'objects': objects, 'page': 'hol',
		'title': 'Feriadu Nacional', 'legend': 'Feriadu Nacional'
	}
	return render(request, 'attendance_custom/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def HolidayAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		newid, _ = getnewid(Holiday)
		form = HolidayForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.save()
			messages.success(request, f'Feriadu nacional amenta ona.')
			return redirect('attend-custom-holiday-list')
	else: form = HolidayForm()
	context = {
		'group': group, 'form': form,
		'title': 'Aumenta Feriadu Nacional', 'legend': 'Aumenta Feriadu Nacional'
	}
	return render(request, 'attendance_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def HolidayUpdate(request, pk):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Holiday, pk=pk)
	if request.method == 'POST':
		form = HolidayForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Feriadu Nacional altera ona.')
			return redirect('attend-custom-holiday-list')
	else: form = HolidayForm(instance=objects)
	context = {
		'group': group, 'form': form,
		'title': 'Altera Feriadu Nacional', 'legend': 'Altera Feriadu Nacional'
	}
	return render(request, 'attendance_custom/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr','hr_s'])
def HolidayDelete(request, pk):
	group = request.user.groups.all()[0].name
	name = None
	objects = get_object_or_404(Holiday, pk=pk)
	name  = objects.name
	objects.delete()
	messages.success(request, f'Feriadu Nacional {name} Apaga Ona')
	return redirect('attend-custom-holiday-list')
###
