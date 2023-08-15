import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision
from leave.models import Leave, LeaveCount, LeaveDE
from leave.forms import LeaveDEForm

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveApprUpdate(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=leave.employee)
	objects = LeaveDE.objects.get(leave=leave)
	if request.method == 'POST':
		form = LeaveDEForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			if instance.obs == 'Sim':
				instance.datetime = datetime.datetime.now()
			instance.save()
			leave.de_approve = True
			leave.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('leave-de-appr-detail', hashid=hashid)
	else: form = LeaveDEForm(instance=objects)
	context = {
		'c_emp': leave.employee, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'de',
		'title': 'Aprovasaun Presidente', 'legend': 'Aprovasaun Presidente'
	}
	return render(request, 'leave/form.html', context)

@login_required
@allowed_users(allowed_roles=['de','deputy'])
def deLeaveApprFinish(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	leavecount = LeaveCount.objects.filter(employee=leave.employee, leave_type=leave.leave_type).last()
	objects = LeaveDE.objects.get(leave=leave)
	if objects.obs == "Sim":
		leave.is_approve = True
		leave.pr_approve = True
		leave.is_reject = False
	elif objects.obs == "Lae":
		leave.is_reject = True
		leave.is_approve = False
		leave.save()
	leave.is_finish = True
	leave.save()
	messages.success(request, f'Aprova sucessu.')
	return redirect('leave-de-appr-detail', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['de'])
def prLeaveSendNotif(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.pr_send = True
	leave.is_finish = True
	leave.save()
	messages.success(request, f'Susesu Notifika Aplikante')
	return redirect('leave-de-appr-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['de'])
def prLeaveNotifyHR(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.pr_notify = True
	leave.save()
	messages.success(request, f'Susesu Notifika RH no Vice Presidente')
	return redirect('leave-de-appr-detail', hashid=hashid)
