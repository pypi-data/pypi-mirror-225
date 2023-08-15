from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import EmpPosition
from employee.models import CurEmpDivision
from settings_app.decorators import allowed_users
from leave.models import Leave, LeaveCount, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeavePrint(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	leavecount = LeaveCount.objects.filter(employee=leave.employee, leave_type=leave.leave_type).first()
	leavedel = LeaveDelegate.objects.filter(leave=leave).first()
	leaveunit = LeaveUnit.objects.filter(leave=leave).first()
	leavehr = LeaveHR.objects.filter(leave=leave).first()
	leavede = LeaveDE.objects.filter(leave=leave).first()
	empdiv = CurEmpDivision.objects.get(employee=leave.employee)
	dep, unit = [],[]
	if empdiv.department:
		dep = EmpPosition.objects.filter(is_active=True, position_id=4, department=empdiv.department).first()
		unit = EmpPosition.objects.filter(is_active=True, position_id=3, unit=empdiv.department.unit).first()
	elif empdiv.unit:
		unit = EmpPosition.objects.filter(is_active=True, position_id=4, unit=empdiv.unit).first()
	de = EmpPosition.objects.filter(is_active=True, position_id=1).first()
	context = {
		'group': group, 'leave': leave, 'leavecount': leavecount, 'leavedel': leavedel, 'leaveunit': leaveunit,
		'leavehr': leavehr, 'leavede': leavede, 'dep': dep, 'unit': unit, 'de': de, 
		'title': 'Imprimi Licensa', 'legend': 'Imprimi Licensa'
	}
	return render(request, 'leave_print/leave_print.html', context)