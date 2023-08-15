from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from leave.models import Leave, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit,LeaveCount,LeaveDep, LeavePeriod, LeaveType, Month
from settings_app.user_utils import c_unit, c_staff
from employee.models import Employee
import pandas as pd
from django.contrib import messages
from contract.models import Contract
from datetime import datetime
import numpy as np
from leave.utils import check_period_date,check_period_range
from django.db.models import QuerySet
from django.template.loader import get_template
from django.http import FileResponse
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
import os
from django.conf import settings
from io import BytesIO
from settings_app.models import IPGInfo


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-start_date')
	period = LeavePeriod.objects.filter(employee=c_emp, is_active=True).last()
		
	context = {
		'group': group, 'objects': objects, 'period':period,
		'title': 'Lista Licensa', 'legend': 'Lista Licensa'
	}
	return render(request, 'leave/hr_cert_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrPeriodList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	year = datetime.now().year
	objects = LeavePeriod.objects.filter(is_active=True).order_by('-is_active')
	context = {
		'group': group, 'objects': objects, 'year': year,
		'title': 'Lista Periode', 'legend': 'Lista Periode'
	}
	return render(request, 'leave/hr_period_list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveCertDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'leavehr': leavehr, 'leavede': leavede,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa'
	}
	return render(request, 'leave/hr_cert_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveAppList(request):
	group = request.user.groups.all()[0].name
	objects = Leave.objects.all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Pedido Licensa', 'legend': 'Lista Pedido Licensa'
	}
	return render(request, 'leave/hr_app_list.html', context)

# done: Leave Raw Data
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveAppRawList(request):
	group = request.user.groups.all()[0].name
	objects = []
	employee = Employee.objects.filter(status_id=1)
	today = datetime.today().date()
	lc = None
	for i in employee:
		period = LeavePeriod.objects.filter(employee=i,is_active=True).last()
		periodcheck = LeavePeriod.objects.all().exists()
		leave = Leave.objects.filter(employee=i)
		alleavelast = LeaveCount.objects.filter(employee=i, period=period, leave_type_id=1, update_date__lt=today).last()
		alleavenext = LeaveCount.objects.filter(employee=i, period=period, leave_type_id=1, update_date__gt=today).first()
		ltabalance = LeaveCount.objects.filter(employee=i, leave_type_id=1, period__is_active=True).last()
		ltsbalance = LeaveCount.objects.filter(employee=i, leave_type_id=2, period__is_active=True).last()
		ltspbalance = LeaveCount.objects.filter(employee=i, leave_type_id=3, period__is_active=True).last()
		ltmbalance = LeaveCount.objects.filter(employee=i, leave_type_id=4, period__is_active=True).last()
		ltpbalance = LeaveCount.objects.filter(employee=i, leave_type_id=5, period__is_active=True).last()
		ltchbalance = LeaveCount.objects.filter(employee=i, leave_type_id=6, period__is_active=True).last()
		lc = LeaveCount.objects.filter(employee=i, period=period).exists()
		leavemonth = Leave.objects.filter(employee=i, leave_period=period, start_date__month=today.month, start_date__year=today.year,leave_type_id=1).exists()
		objects.append([i,leave, ltabalance, ltsbalance, ltspbalance, ltmbalance, ltpbalance, lc, ltchbalance,alleavelast,alleavenext,leavemonth])
		
	context = {
		'group': group, 'objects': objects,  'lc':lc, 'periodcheck':periodcheck,
		'title': 'Lista Raw Data Licenca', 'legend': 'Lista Raw Data Licenca', 'today':today
	}
	return render(request, 'leave/hr_raw_list.html', context)


# work: Work here
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveRecordPer(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	if contract:
		try:
			today = datetime.today().date()
			period  = get_object_or_404(LeavePeriod, employee=employee, is_active=True)
			leave = Leave.objects.filter(employee=employee, leave_period=period).order_by('-start_date')
			
			min_month = f'{period.start_year.year}-{period.start_month.code}-{period.start_date.day}'
			max_month = f'{today.year}-{today.month}-{period.start_date.day}'
			months = pd.date_range(min_month, max_month, freq='M')
			check_last_period = LeavePeriod.objects.filter(employee=employee,pk__lt=period.pk).last()
			all_period = LeavePeriod.objects.filter(employee=employee)
			last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
			lc = LeaveCount.objects.filter(employee=employee, period=period).exists()
			data = []
			data2 = []
			allmonth = check_period_range(period)
			for obj in allmonth:
				al = LeaveCount.objects.filter(employee=employee, period=period,  month__code=obj.month, year__year=obj.year, leave_type_id=1).last()
				sl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=2).last()
				spl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=3).last()
				mtl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=4).last()
				ptl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=5).last()
				cl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=6).last()
				lmonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=obj.month, start_date__year=obj.year,leave_type_id=1).exists()

				data2.append([obj, al,sl, spl, mtl, ptl, cl, lmonth])
			objects = []
			alleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1).last()
			alleavelast = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__lt=today).last()
			alleavenext = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__gt=today).first()
			alleavethis = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__month=today.month, update_date__year=today.year).last()

			sickleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=2).all().order_by('pk')
			spleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=3).all().order_by('pk')
			mtleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=4).all().order_by('pk')
			ptleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=5).all().order_by('pk')
			chleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=6).all().order_by('pk')
			leavecheck = LeaveCount.objects.filter(employee=employee, period=period, period__employee=employee ).exists()
			leavemonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=today.month, start_date__year=today.year,leave_type_id=1).exists()
			objects.append([alleave, spleave,sickleave, mtleave, ptleave,chleave, data, leavemonth, alleavelast,alleavenext, alleavethis])

			check_date = check_period_date(period.start_date)
			check_last_month_per = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1,  month__code=1, year__year=2023).exists()

			context = {
				'group': group, 'employee':employee, 'alleave':alleave, 'period':period, 'leave':leave, 'last_count_period':last_count_period, 'today':check_date,
				'title': 'Leave Record', 'legend': 'Leave Record', 'objects': objects, 'leavecheck':leavecheck, 'all_period':all_period, 'contract':contract, \
				'check_last_month_per':check_last_month_per, 'today':today,'allmonth':allmonth, 'data':data2, 'today':today, 'lc':lc
			}
			return render(request, 'leave/hr_leave_record.html', context)				
		except:
			if contract.start_date:
				context = {
					'legend': 'Leave Record', 'employee':employee, 'contract': contract
				}
				return render(request, 'leave/hr_leave_record.html', context)				
			else:
				messages.error(request, 'Contrato seidauk kria!!')
				return redirect('leave-hr-app-raw-list')	
	else:
		messages.error(request, f'Funsionario {employee} nia Kontrato seidauk kria!!')
		return redirect('leave-hr-app-raw-list')	

	

# work: Work here
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeavePeriodRecordPer(request, hashid, pk):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	period  = get_object_or_404(LeavePeriod, pk=pk)
	today = datetime.today().date()
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	leave = Leave.objects.filter(employee=employee, leave_period=period).order_by('-start_date')
	min_month = f'{period.start_year.year}-{period.start_month.code}-{period.start_date.day}'
	max_month = f'{today.year}-{today.month}-{period.start_date.day}'
	months = pd.date_range(min_month, max_month, freq='M')
	check_last_period = LeavePeriod.objects.filter(employee=employee,pk__lt=period.pk).last()
	all_period = LeavePeriod.objects.filter(employee=employee)
	last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
	lc = LeaveCount.objects.filter(employee=employee, period=period).exists()
	data = []
	data2 = []
	allmonth = check_period_range(period)
	for obj in allmonth:
		al = LeaveCount.objects.filter(employee=employee, period=period,  month__code=obj.month, year__year=obj.year, leave_type_id=1).last()
		sl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=2).last()
		spl = LeaveCount.objects.filter(employee=employee, period=period, month__code=obj.month, year__year=obj.year, leave_type_id=3).last()
		mtl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=4).last()
		ptl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=5).last()
		cl = LeaveCount.objects.filter(employee=employee, period=period,month__code=obj.month, year__year=obj.year, leave_type_id=6).last()
		lmonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=obj.month, start_date__year=obj.year,leave_type_id=1).exists()

		data2.append([obj, al,sl, spl, mtl, ptl, cl, lmonth])
	objects = []
	alleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1).last()
	alleavelast = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__lt=today).last()
	alleavenext = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__gt=today).first()
	alleavethis = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1, update_date__month=today.month, update_date__year=today.year).last()

	sickleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=2).all().order_by('pk')
	spleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=3).all().order_by('pk')
	mtleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=4).all().order_by('pk')
	ptleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=5).all().order_by('pk')
	chleave = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=6).all().order_by('pk')
	leavecheck = LeaveCount.objects.filter(employee=employee, period=period, period__employee=employee ).exists()
	leavemonth = Leave.objects.filter(employee=employee, leave_period=period, start_date__month=today.month, start_date__year=today.year,leave_type_id=1).exists()
	objects.append([alleave, spleave,sickleave, mtleave, ptleave,chleave, data, leavemonth, alleavelast,alleavenext, alleavethis])

	check_date = check_period_date(period.start_date)
	check_last_month_per = LeaveCount.objects.filter(employee=employee, period=period, leave_type_id=1,  month__code=1, year__year=2023).exists()
		
	context = {
			'group': group, 'employee':employee, 'alleave':alleave, 'period':period, 'leave':leave, 'last_count_period':last_count_period, 'today':check_date,
			'title': 'Leave Record', 'legend': 'Leave Record', 'objects': objects, 'leavecheck':leavecheck, 'all_period':all_period, 'contract':contract, \
			'check_last_month_per':check_last_month_per, 'today':today,'allmonth':allmonth, 'data':data2, 'today':today, 'lc':lc, 'page': 'list-year'
	}
	return render(request, 'leave/hr_leave_record.html', context)




@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveAppDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	emp_unit = c_unit(leave.employee.employeeuser.user)
	cgroup = leave.user.groups.all()[0].name
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leavedep = LeaveDep.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'leavehr': leavehr, 'leavede': leavede, 'leavedep':leavedep, 'emp_unit':emp_unit,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa', 'cgroup':cgroup
	}
	return render(request, 'leave/hr_app_detail.html', context)

import os

def get_image_path(image_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'main', 'static', 'main', 'images', image_name)
    return image_path


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeavePDF(request, hashid):
	today = datetime.today().date()
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	cgroup = leave.user.groups.all()[0].name
	leavedep = LeaveDep.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	ipginfo = IPGInfo.objects.filter(is_active=True).last()
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'inline; filename="Leave_{leave.employee.first_name}_ON_{leave.start_date.day}_{leave.start_date.month}_{leave.start_date.year}.pdf"'
	template = get_template('pdf/leave.html')
	host_url = request.get_host()
	path = f'{host_url}/media/{ipginfo.image}'
	if leave.leave_type.pk == 1:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period,update_date__lte=today, leave_type=leave.leave_type).last()
	else:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period, leave_type=leave.leave_type).last()

	context = {
		'mpm_path': 'main/static/main/images/mpm.png',
		'ipg_path': 'http://'+path,
		'title': 'PDF Licensa', 'cgroup':cgroup, 'leave_count':leave_count, 
		'leavedep':leavedep, 'leaveunit':leaveunit, 'leavehr':leavehr,
		'leavede':leavede, 'leave':leave, 'ipginfo':ipginfo
	}
	html = template.render(context)

	pisaStatus = pisa.CreatePDF(html, dest=response)

	return response

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


def hrLeaveAproveList(request):
	group = request.user.groups.all()[0].name
	current_date = datetime.now()
	default_month = current_date.month
	default_year = current_date.year
	start_date = request.GET.get('start_date')
	end_date = request.GET.get('end_date')

	date_range_query = {}
	if start_date and end_date:
		start_date = datetime.strptime(start_date, "%Y-%m-%d")
		end_date = datetime.strptime(end_date, "%Y-%m-%d")
		date_range_query['start_date__range'] = (start_date, end_date)

	objects = Leave.objects.filter(is_approve=True, **date_range_query).order_by('-start_date')
	ipginfo = IPGInfo.objects.filter(is_active=True).last()
	host_url = request.get_host()
	path = f'{host_url}/media/{ipginfo.cop}'
	current_year = datetime.now().year
	years = [year for year in range(2012, current_year + 1)]

	context = {
		'group': group,
		'objects': objects,
		'title': 'Lista Licensa Aprovado',
		'legend': 'Lista Licensa Aprovado',
		'years': years,
		'months': Month.objects.all(),
		'default_month': default_month,
		'default_year': default_year,
		'start_date': start_date,
		'end_date': end_date,
		'page': 'approve',
		'path':path
	}
	return render(request, 'leave/hr_approve_list.html', context)
