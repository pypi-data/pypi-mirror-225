from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from leave.models import Leave, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit
from settings_app.user_utils import c_unit

@login_required
@allowed_users(allowed_roles=['unit'])
def cLeaveVerList(request):
	group = request.user.groups.all()[0].name
	emp_unit, unit = c_unit(request.user)
	objects = Leave.objects.filter(
		Q((Q(employee__curempdivision__department__unit=unit)|\
        Q(employee__curempdivision__unit=unit)),dep_send=True, is_finish=False)|
		Q((Q(employee__curempdivision__department__unit=unit)|\
        Q(employee__curempdivision__unit=unit)),is_send_to_div=True, is_finish=False, is_cancel=False)

	).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa hodi Aprova', 'legend': 'Lista Licensa hodi Aprova'
	}
	return render(request, 'leave/c_ver_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit'])
def cLeaveVerDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa'
	}
	return render(request, 'leave/c_ver_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['unit', 'deputy'])
def cLeaveList(request):
	group = request.user.groups.all()[0].name
	c_emp, unit = c_unit(request.user)
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa', 'legend': 'Lista Licensa'
	}
	return render(request, 'leave/c_apply_list.html', context)

@login_required
@allowed_users(allowed_roles=['unit', 'deputy'])
def cLeaveDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	cgroup = leave.employee.employeeuser.user.groups.all()[0].name
	leavede = LeaveDE.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'leavehr': leavehr, 'leavede': leavede, 'cgroup':cgroup,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa'
	}
	return render(request, 'leave/c_apply_detail.html', context)