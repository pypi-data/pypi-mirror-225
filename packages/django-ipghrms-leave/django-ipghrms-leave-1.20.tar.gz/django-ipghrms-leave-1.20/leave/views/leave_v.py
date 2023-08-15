from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.db.models import Sum, Count, Q
from leave.models import Leave, LeaveDelegate, LeaveDep, LeaveHR, LeaveUnit
from settings_app.user_utils import c_staff, c_dep
from employee.models import CurEmpDivision

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LeaveList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Licensa', 'legend': 'Lista Licensa'
	}
	return render(request, 'leave/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LeaveDetail(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	context = {
		'group': group, 'objects': objects,
		'title': 'Detalha Licensa', 'legend': 'Detalha Licensa'
	}
	return render(request, 'leave/detail.html', context)
###
@login_required
# @allowed_users(allowed_roles=['staff'])
def LeaveDelegList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_dep(request.user)
	objects = LeaveDelegate.objects.filter(employee=c_emp).all().order_by('-leave__start_date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Aplikasaun Licensa', 'legend': 'Lista Aplikasaun Licensa'
	}
	return render(request, 'leave/deleg_list.html', context)

# work: Leave DEP
@login_required
@allowed_users(allowed_roles=['dep'])
def LeaveDepList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = []
	objects = Leave.objects.filter(employee=c_emp).all().order_by('-pk')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Aplikasaun', 'legend': 'Lista Aplikasaun'
	}
	return render(request, 'leave/dep_list.html', context)

@login_required
@allowed_users(allowed_roles=['dep'])
def LeaveDepAprvList(request):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	objects = []
	objects = LeaveDep.objects.filter(leave__employee__curempdivision__department=c_emp.curempdivision.department).all().order_by('-pk')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Predido Aprovasaun Lisensa', 'legend': 'Lista Predido Aprovasaun Lisensa'
	}
	return render(request, 'leave/dep_req_list.html', context)

@login_required
@allowed_users(allowed_roles=['dep'])
def LeaveDepDetail(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leavedep = get_object_or_404(LeaveDep, hashed=hashid)
	leave = leavedep.leave
	leavehr = get_object_or_404(LeaveHR, leave=leave)
	leaveunit = get_object_or_404(LeaveUnit, leave=leave)
	cgroup = leave.user.groups.all()[0].name
	context = {
		'group': group, 'leave': leave, 'leavedep': leavedep, 'empdiv':empdiv, 'leavehr':leavehr, 'leaveunit':leaveunit,
		'title': 'Detalha Pedido Aplikasaun Licensa', 'legend': 'Detalha Pedido Aplikasaun Licensa', 'cgroup':cgroup
	}
	return render(request, 'leave/dep_detail.html', context)



@login_required
# @allowed_users(allowed_roles=['staff'])
def LeaveDelegDetail(request, hashid):
	group = request.user.groups.all()[0].name
	leavedel = get_object_or_404(LeaveDelegate, hashed=hashid)
	leave = leavedel.leave
	context = {
		'group': group, 'leave': leave, 'leavedel': leavedel,
		'title': 'Delegasaun Servisu', 'legend': 'Delegasaun Servisu'
	}
	return render(request, 'leave/deleg_detail.html', context)