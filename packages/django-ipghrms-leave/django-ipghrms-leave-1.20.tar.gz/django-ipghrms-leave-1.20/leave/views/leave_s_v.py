from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from leave.models import Leave, LeaveCount, LeaveDE, LeaveDelegate, LeaveHR, LeaveType, LeaveUnit, LeaveDep, LeavePeriod
from settings_app.user_utils import c_dep, c_staff, c_unit
from django.contrib import messages
from datetime import datetime
from settings_app.models import IPGInfo
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from django.template.loader import get_template
from employee.models import EmpSignature

@login_required
@allowed_users(allowed_roles=['staff','dep', 'hr'])
def sLeaveList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa', 'legend': 'Lista Licensa'
	}
	return render(request, 'leave/s_apply_list.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep', 'hr'])
def sLeaveDetail(request, hashid):
	today = datetime.today().date()
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leavedep = LeaveDep.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	if leave.leave_type.pk == 1:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period,update_date__lte=today, leave_type=leave.leave_type).last()
	else:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period, leave_type=leave.leave_type).last()

	# print(leave_count)
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'leavehr': leavehr, 'leavede': leavede,'leavedep':leavedep, 'leave_count':leave_count,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa'
	}
	return render(request, 'leave/s_apply_detail.html', context)

@login_required
@allowed_users(allowed_roles=['staff','dep'])
def LeaveTerminate(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.is_done = True
	leave.save()
	messages.success(request, 'Susesu Termina Licensa')
	if group == 'staff':
		return redirect('leave-s-list')
	if group == 'dep':
		return redirect('leave-dep-list')
###
@login_required
def sLeaveBalCheck(request):
	group = request.user.groups.all()[0].name
	today = datetime.today().date()
	page = ''
	c_emp = []
	if group == "staff":
		c_emp = c_staff(request.user)
		page = 'cstaff'
	elif group == "dep":
		c_emp, _ = c_dep(request.user)
		page = 'cdep'
	elif group == "unit":
		c_emp, _ = c_unit(request.user)
		page = 'cunit'
	elif group == "de":
		c_emp, _ = c_unit(request.user)
		page = 'cde'
	elif group == "deputy":
		c_emp, _ = c_unit(request.user)
		page = 'cdeputy'
	else:
		c_emp, _ = c_unit(request.user)
	period = LeavePeriod.objects.filter(employee=c_emp, is_active=True).last()
	if period:
		if c_emp.sex == 'Female':
			leavetypes = LeaveType.objects.all()
			objects = []
		else:
			leavetypes = LeaveType.objects.exclude(pk=4)
			objects = []

		for i in leavetypes:
			if i.pk == 1:
				a = LeaveCount.objects.filter(employee=c_emp, period__is_active=True, update_date__lte=today, period__employee=c_emp,  leave_type=i).last()
				objects.append([i,a])
			else:
				a = LeaveCount.objects.filter(employee=c_emp, period__is_active=True, period__employee=c_emp,  leave_type=i).last()
				objects.append([i,a])

		context = {
			'group': group, 'c_emp': c_emp, 'objects': objects, 'page': page,
			'title': 'Lista Balansu Licensa', 'legend': 'Lista Balansu Licensa'
		}
		return render(request, 'leave/bal_s_list.html', context)
	else:
		messages.error(request, 'Periode Licensa seidauk kria. Halo Favor Kontakto Rekurso Humano')
		if group == "staff": return redirect('leave-s-list')
		if group == "dep": return redirect('leave-dep-list')
		elif group == "unit": return redirect('leave-c-list')
		elif group == "de": return redirect('leave-de-list')
		elif group == "deputy": return redirect('leave-de-list')
		elif group == "hr": return redirect('leave-hr-list')


@login_required
@allowed_users(allowed_roles=['staff','unit', 'dep', 'deputy', 'de'])
def sLeavePDF(request, hashid):
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
	if leave.leave_type.pk == 1:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period,update_date__lte=today, leave_type=leave.leave_type).last()
	else:
		leave_count = LeaveCount.objects.filter(employee=leave.employee, period=leave.leave_period, leave_type=leave.leave_type).last()

	signature = None
	if leavede.user:
		signature = EmpSignature.objects.filter(employee=leavede.user.employeeuser.employee).last()
	if leaveunit.user:
		signature = EmpSignature.objects.filter(employee=leaveunit.user.employeeuser.employee).last()

	response['Content-Disposition'] = f'inline; filename="Leave_ON_{leave.start_date.day}_{leave.start_date.month}_{leave.start_date.year}.pdf"'
	template = get_template('pdf/leave.html')
	host_url = request.get_host()
	path = f'{host_url}/media/{ipginfo.image}'
	signature_path = ''
	if signature:
		signature_path = f'{host_url}/media/{signature.image}'
	context = {
		'mpm_path': 'main/static/main/images/mpm.png',
		'ipg_path': 'http://'+path,
		'signature_path': 'https://'+signature_path,
		'title': 'PDF Licensa', 'cgroup':cgroup,  'leave_count':leave_count,
		'leavedep':leavedep, 'leaveunit':leaveunit, 'leavehr':leavehr,
		'leavede':leavede, 'leave':leave, 'ipginfo':ipginfo
	}
	html = template.render(context)

	pisaStatus = pisa.CreatePDF(html, dest=response)

	return response