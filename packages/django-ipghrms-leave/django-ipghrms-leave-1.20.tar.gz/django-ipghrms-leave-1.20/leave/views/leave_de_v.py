from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from leave.models import Leave, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit,LeaveDep
from settings_app.user_utils import c_unit, c_staff

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveApprList(request):
	group = request.user.groups.all()[0].name
	objects = Leave.objects.filter((Q(dep_send_pr=True)|Q(unit_send_pr=True)), is_finish=False, is_cancel=False).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa hodi Aprova', 'legend': 'Lista Pedido Husu Aprovasaun Licensa'
	}
	return render(request, 'leave/de_appr_list.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa', 'legend': 'Lista Licensa'
	}
	return render(request, 'leave/de_list.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	cgroup = leave.user.groups.all()[0].name
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavedep = LeaveDep.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
        'leavehr': leavehr, 'leavede': leavede, 'leavedep': leavedep,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa', 'cgroup':cgroup
	}
	return render(request, 'leave/de_detail.html', context)
@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveApprDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	cgroup = leave.user.groups.all()[0].name
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavedep = LeaveDep.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel, 'leaveunit': leaveunit,
        'leavehr': leavehr, 'leavede': leavede, 'leavedep': leavedep,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa', 'cgroup':cgroup
	}
	return render(request, 'leave/de_appr_detail.html', context)