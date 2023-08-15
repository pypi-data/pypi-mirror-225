import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision, Employee
from leave.models import Leave, LeaveCount, LeaveUnit, LeaveDep
from leave.forms import LeaveUnitForm, LeaveDepForm
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_dep

@login_required
@allowed_users(allowed_roles=['unit'])
def cLeaveVerUpdate(request, hashid):
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leave = get_object_or_404(Leave, hashed=hashid)
	objects = LeaveUnit.objects.get(leave=leave)
	if request.method == 'POST':
		form = LeaveUnitForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			if instance.obs == 'Sim':
				instance.datetime = datetime.datetime.now()
				leave.is_approve = True
				leave.unit_confirm = True
				leave.save()
			else:
				instance.datetime = datetime.datetime.now()
				leave.save()
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('leave-c-ver-detail', hashid=hashid)
	else: form = LeaveUnitForm(instance=objects)
	context = {
		'c_emp': c_emp, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'unit',
		'title': 'Verfika husi Unidade', 'legend': 'Verfika husi Unidade'
	}
	return render(request, 'leave/form.html', context)

# workd: Leave Dep
@login_required
@allowed_users(allowed_roles=['dep'])
def cLeaveDepUpdate(request, hashid):
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leave = get_object_or_404(Leave, hashed=hashid)
	emp = leave.employee
	objects = LeaveDep.objects.get(leave=leave)
	if request.method == 'POST':
		form = LeaveDepForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			leave.dep_confirm = True
			leave.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('leave-dep-detail', hashid=leave.leavedep.hashed)
	else: form = LeaveDepForm(instance=objects)
	context = {
		'c_emp': c_emp, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'unit',
		'title': 'Desizaun husi Chefe Ekipa', 'legend': 'Desizaun husi Chefe Ekipa', 'emp': emp
	}
	return render(request, 'leave/form.html', context)
@login_required
@allowed_users(allowed_roles=['dep'])
def cLeaveDepSend(request, hashid):
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leave = get_object_or_404(Leave, hashed=hashid)
	if empdiv.unit.pk == 8 or empdiv.department.unit.pk == 8:
		leave.dep_send_pr = True
		leave.hr_confirm = False
		leave.save()
	else:
		leave.dep_send = True
		leave.hr_confirm = False
		leave.save()
	messages.success(request, f'Susesu Manda Ona')
	return redirect('leave-dep-detail', hashid=leave.leavedep.hashed)


@login_required
@allowed_users(allowed_roles=['unit'])
def cLeaveVerSend(request, hashid):
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.unit_send = True
	leave.is_finish = True
	leave.hr_confirm = False
	leave.save()
	messages.success(request, f'Manda sucessu.')
	return redirect('leave-c-ver-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dep', 'unit'])
def cLeaveVerReject(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.is_finish = True
	leave.is_reject = True
	leave.save()
	# leavecount = LeaveCount.objects.filter(employee=leave.employee, leave_type=leave.leave_type).last()
	# leavecount.total = leavecount.total - leave.days
	# leavecount.balance = leavecount.balance + leave.days
	# leave.save()
	messages.success(request, f'Susesu Notifika Aplikante')
	if group == 'dep':
		return redirect('leave-dep-detail', hashid=leave.leavedep.hashid)
	elif group == 'unit':
		return redirect('leave-c-ver-detail', hashid=hashid)
