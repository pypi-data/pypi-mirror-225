import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision, Employee
from leave.models import Leave, LeaveHR, LeaveUnit, LeaveCount, LeavePeriod, Month as Mnth, Year as Yr, LeaveType
from leave.forms import LeaveHRForm, LeaveUnitForm, LeaveForm, HRLeaveForm, HRPeriodForm, HRLeaveCommentForm
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_unit
from dateutil.parser import parser
from datetime import datetime as dt
from datetime import timedelta
from attendance.models import Attendance, AttendanceStatus,Year, Month
import pytz
import pandas as pd
from django.db.models import Q, F
from django.utils import timezone
from calendar import mdays
from attendance.models import Attendance, AttendanceStatus, Year as YAten, Month as Maten
from leave.utils import createAttendance, createLeave
from contract.models import Contract


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveCertUpdate(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=leave.employee)
	objects = LeaveHR.objects.get(leave=leave)
	if request.method == 'POST':
		form = LeaveHRForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = timezone.now()
			instance.user = request.user
			instance.save()
			leave.hr_confirm = True
			leave.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('leave-hr-cert-detail', hashid=hashid)
	else: form = LeaveHRForm(instance=objects)
	context = {
		'c_emp': leave.employee, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'hr',
		'title': 'Certifikasaun RH', 'legend': 'Certifikasaun RH'
	}
	return render(request, 'leave/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveAddComment(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	empdiv = CurEmpDivision.objects.get(employee=leave.employee)
	objects = LeaveHR.objects.get(leave=leave)
	if request.method == 'POST':
		form = HRLeaveCommentForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = timezone.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Susesu fo komentario')
			return redirect('leave-hr-app-detail', hashid=hashid)
	else: form = HRLeaveCommentForm(instance=objects)
	context = {
		'c_emp': leave.employee, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'hr',
		'title': 'Fo Komentario', 'legend': 'Fo Komentario'
	}
	return render(request, 'leave/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveCertSend(request, hashid):
	leave = get_object_or_404(Leave, hashed=hashid)
	leave.hr_send = True
	leave.de_approve = False
	leave.save()
	messages.success(request, f'Manda sucessu.')
	return redirect('leave-hr-cert-detail', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveUpdateEmpRecord(request, hashid):
	employee = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	if contract:
		leave_type = None
		if employee.sex == 'Male':
			leave_type = LeaveType.objects.exclude(pk=4)
		else:
			leave_type = LeaveType.objects.all()
		today = dt.today().date()
		leave_period = LeavePeriod.objects.filter(is_active=True, employee=employee).last()
		check_last_period = LeavePeriod.objects.filter(pk__lt=leave_period.pk, employee=employee).last()
		last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
		last_month_date = today.replace(day=1) - timedelta(days=1)
		min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}-{leave_period.start_date.day}'
		max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'

		months = pd.period_range(min_month, max_month, freq='M')
		i = 0
		while i < len(months):
			leave_check = LeaveCount.objects.filter(employee=employee, period=leave_period).last()
			m = months[i]
			get_m = get_object_or_404(Mnth, code=m.month)
			get_y = get_object_or_404(Yr, year=m.year)
			if leave_check:
				for lt1 in leave_type:
					if lt1.pk == 1:
						print('CALLLL 1')
						lastleaveal = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type_id=1).last()
						earn_per_month = round(float(lt1.total/12),2)
						date_period_string = f"{m.year}-{m.month}-{leave_period.start_date.day}"
						date_period = dt.strptime(date_period_string,"%Y-%m-%d").date()
						lcnew = LeaveCount.objects.create(
							period = leave_period,
							employee=employee,
							leave_type=lt1,
							month = get_m,
							year = get_y,
							update_date=date_period,
							leave_earn = earn_per_month
						)
						lcnew.balance = round(float(lastleaveal.balance) + float(lcnew.leave_earn) - float(lcnew.taken),2)
						lcnew.total_earn = round(float(lastleaveal.prov_total_earn) + float(lcnew.leave_earn),1)
						lcnew.total_balance = round(float(lcnew.total_earn) - float(lcnew.total_taken),1)
						lcnew.balance_carry = lcnew.total_balance
						lcnew.total_balance_leave = float(lt1.total) - float(lcnew.total_balance)
						lcnew.prov_total_earn = float(lastleaveal.prov_total_earn) + float(earn_per_month)
						lcnew.balance_month = round(float(lastleaveal.total_balance) - float(lcnew.taken),2)
						lcnew.save()
			else:
				for lt in leave_type:
					if lt.pk == 1:
						# work: Check Balansu iha Periode Kotuk
						date_period_string = f"{m.year}-{m.month}-{leave_period.start_date.day}"
						date_period = dt.strptime(date_period_string,"%Y-%m-%d").date()
						if check_last_period:
							print('CALLLL HEREE LAST PERIOD')
							earn_per_month = round(float(lt.total/12),2)

							lc = LeaveCount.objects.create(
								period = leave_period,
								employee=employee,
								leave_type=lt,
								month = get_m,
								year = get_y,
								update_date=date_period,
								leave_earn = earn_per_month
							)
							lc.balance = round(float(last_count_period.total_balance) +   float(lc.leave_earn) - float(lc.taken),2)
							lc.total_earn = round(float(lc.leave_earn) + float(last_count_period.total_balance),2)
							lc.total_balance = round(float(lc.total_earn) - float(lc.total_taken),2)
							lc.balance_carry = lc.total_balance
							lc.total_balance_leave = float(lt.total) - float(lc.total_balance)
							lc.prov_total_earn = lc.total_earn
							lc.balance_month = round(float(lc.total_balance) - float(lc.taken),2)
							lc.save()
						else:
							print('CALLLL HEREE LAST PERIOD ELSEE')
							earn_per_month = round(float(lt.total/12),2)
							# balance_per_month = round(float(earn_per_month) - float(taken),2)

							lc = LeaveCount.objects.create(
								period = leave_period,
								employee=employee,
								leave_type=lt,
								month = get_m,
								year = get_y,
								update_date=date_period,
								leave_earn = earn_per_month
							)
							lc.balance = round(float(lc.leave_earn) - float(lc.taken),2)
							lc.total_earn = round(float(lc.leave_earn),2)
							lc.total_balance = round(float(lc.balance),2)
							lc.balance_carry = lc.total_balance
							lc.total_balance_leave = float(lt.total) - float(lc.total_balance)
							lc.prov_total_earn = lc.leave_earn
							lc.balance_month = round(float(lc.balance) - float(lc.taken),2)
							lc.save()
					else:
						lcall = LeaveCount.objects.create(
							period = leave_period,
							employee=employee,
							leave_type=lt,
							year = get_y,
						)
						lcall.total_balance = float(lt.total)
						lcall.save()
			
			i+=1
		messages.success(request, f'Susesu Update Record')
		return redirect('leave-hr-leave-record', hashid=hashid)
	else:
		messages.error(request, f'Kontrato ba pessoal refere seidauk iha!!')
		return redirect('leave-hr-leave-record', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveUpdateRecord(request):
	employee = Employee.objects.filter(status_id=1)
	for emp in employee:
		# work: Get Last Employee Leave Count
		leave_type = None
		if emp.sex == 'Male':
			leave_type = LeaveType.objects.exclude(pk=4)
		else:
			leave_type = LeaveType.objects.all()
		leave_type_al = LeaveType.objects.get(pk=1)
		leave_period = LeavePeriod.objects.filter(is_active=True, employee=emp).last()
		# work: Depois koko tan ida tan
		check_last_period = LeavePeriod.objects.filter(pk__lt=leave_period.pk, employee=emp).last()
		last_count_period = LeaveCount.objects.filter(employee=emp, period=check_last_period, leave_type_id=1).last()
		min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
		max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
		months = pd.period_range(min_month, max_month, freq='M')
		i = 0
		while i < len(months):
			leave_check = LeaveCount.objects.filter(employee=emp, period=leave_period).last()
			m = months[i]
			get_m = get_object_or_404(Mnth, code=m.month)
			get_y = get_object_or_404(Yr, year=m.year)
			if leave_check:
				for lt1 in leave_type:
					if lt1.pk == 1:
						lastleaveal = LeaveCount.objects.filter(employee=emp, period=leave_period, leave_type_id=1).last()
						earn_per_month = round(float(lt1.total/12),2)
						date_period_string = f"{m.year}-{m.month}-{leave_period.start_date.day}"
						date_period = dt.strptime(date_period_string,"%Y-%m-%d").date()
						lcnew = LeaveCount.objects.create(
							period = leave_period,
							employee=emp,
							leave_type=lt1,
							month = get_m,
							year = get_y,
							update_date = date_period,
							leave_earn = earn_per_month
						)
						lcnew.balance = round(float(lastleaveal.balance) + float(lcnew.leave_earn) - float(lcnew.taken),2)
						lcnew.total_earn = round(float(lastleaveal.prov_total_earn) + float(lcnew.leave_earn),1)
						lcnew.total_balance = round(float(lcnew.total_earn) - float(lcnew.total_taken),1)
						lcnew.balance_carry = lcnew.total_balance
						lcnew.total_balance_leave = float(lt1.total) - float(lcnew.total_balance)
						lcnew.prov_total_earn = float(lastleaveal.prov_total_earn) + float(earn_per_month)
						lcnew.balance_month = round(float(lastleaveal.balance) - float(lcnew.taken),2)
						lcnew.save()
			else:
				for lt in leave_type:
					if lt.pk == 1:
						# work: Check Balansu iha Periode Kotuk
						date_period_string = f"{m.year}-{m.month}-{leave_period.start_date.day}"
						date_period = dt.strptime(date_period_string,"%Y-%m-%d").date()
						if check_last_period:
							earn_per_month = round(float(lt.total/12),2)

							lc = LeaveCount.objects.create(
								period = leave_period,
								employee=emp,
								leave_type=lt,
								month = get_m,
								year = get_y,
								update_date=date_period,
								leave_earn = earn_per_month
							)
							lc.balance = round(float(lc.leave_earn) - float(lc.taken),2)
							lc.total_earn = round(float(lc.leave_earn) + float(last_count_period.total_balance),2)
							lc.total_balance = round(float(lc.total_earn) - float(lc.total_taken),2)
							lc.balance_carry = lc.total_balance
							lc.total_balance_leave = float(lt.total) - float(lc.total_balance)
							lc.prov_total_earn = lc.total_earn
							lc.balance_month = round(float(lc.balance) - float(lc.taken),2)
							lc.save()
						else:
							earn_per_month = round(float(lt.total/12),2)
							# balance_per_month = round(float(earn_per_month) - float(taken),2)

							lc = LeaveCount.objects.create(
								period = leave_period,
								employee=emp,
								leave_type=lt,
								month = get_m,
								year = get_y,
								update_date=date_period,
								leave_earn = earn_per_month
							)
							lc.balance = round(float(lc.leave_earn) - float(lc.taken),2)
							lc.total_earn = round(float(lc.leave_earn),2)
							lc.total_balance = round(float(lc.balance),2)
							lc.balance_carry = lc.total_balance
							lc.total_balance_leave = float(lt.total) - float(lc.total_balance)
							lc.prov_total_earn = lc.leave_earn
							lc.balance_month = round(float(lc.balance) - float(lc.taken),2)
							lc.save()
					else:
						lcall = LeaveCount.objects.create(
							period = leave_period,
							employee=emp,
							leave_type=lt,
							year = get_y,
						)
						lcall.total_balance = float(lt.total)
						lcall.save()
			i+=1
	messages.success(request, f'Susesu Update Record')
	return redirect('leave-hr-app-raw-list')
	

def update_leave_count(alldata, month):

	for obj in alldata:
		print(obj)


@login_required
def hrLeaveAdd(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	leave_period = LeavePeriod.objects.filter(employee=employee,is_active=True).last()
	check_last_period = LeavePeriod.objects.filter(employee=employee, is_active=True, pk__lt=leave_period.pk).last()
	last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
	min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
	max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
	months = pd.period_range(min_month, max_month, freq='M')
	c_emp = employee
	emp = employee
	if request.method == 'POST':
		newid, new_hashid = getnewid(Leave)
		newsid2, _ = getnewid(LeaveCount)
		form = HRLeaveForm(request.POST, request.FILES)
		if form.is_valid():
			leave_type = form.cleaned_data.get('leave_type')
			days = form.cleaned_data.get('days')
			days = round(float(days),2)
			if leave_type.pk == 1:
				earn_per_month = round(float(leave_type.total/12),2)
			else: earn_per_month = 0.00
			start_date = form.cleaned_data.get('start_date')
			end_date = form.cleaned_data.get('end_date')
			last_two_digits = str(days).split('.')[1][:2]
			last_two_digits = int(last_two_digits)

			min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
			max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
			date1 = pd.to_datetime(start_date, format="%Y %m").date()
			date2 = pd.to_datetime(end_date, format="%Y %m").date()

			start_date_period = pd.to_datetime(min_month, format="%Y %m").date()
			end_date_period = pd.to_datetime(max_month, format="%Y %m").date()
			start_month = date1


			if days <= leave_type.total:
				# done: CHECK ANGKA LORON 0.5/1.0/1.5
				if last_two_digits == int(5) or last_two_digits == int(0):
					# done: CHECK DATA LEAVE IHA PERIODO NIA LARAN
					if start_date_period <= start_month <= end_date_period + datetime.timedelta(days=29):
						# done: CHECK LEAVE TYPE BA ANNUAL
						if leave_type.pk == 1:
							print('ADDD  CALL 1')
							# done: CHECK RECORD IHA FULAN IDA NE'E
							current_leave_count = get_object_or_404(LeaveCount, period=leave_period, employee=employee,leave_type= leave_type, month__code=start_date.month, year__year=start_date.year)
							previous_leave_count = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type= leave_type, month__code__lt=start_date.month, year__year=current_leave_count.year.year).last()
							# done: CHECK KARIK LEAVE IHA FULAN KLARAN
							if previous_leave_count:
								# print('ADDD  CALL 2')
								# if check_last_period:
								# 	print('ADDD  CALL 3')
								# 	current_leave_count.taken = round(float(current_leave_count.taken) + days,2)
								# 	current_leave_count.total_taken = round(float(previous_leave_count.taken) + days)
								# 	current_leave_count.balance = round(float(previous_leave_count.balance) + float(current_leave_count.leave_earn) - float(days),2 )
								# 	current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
								# 	current_leave_count.balance_month = round(float(previous_leave_count.balance) - float(current_leave_count.taken),2)
								# 	current_leave_count.save()
								# else:
								current_leave_count.taken = round(float(current_leave_count.taken) + days,2)
								current_leave_count.total_taken = round(float(previous_leave_count.taken) + days)
								current_leave_count.balance = round(float(previous_leave_count.balance) + float(current_leave_count.leave_earn) - float(days),2 )
								current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
								current_leave_count.balance_month = round(float(previous_leave_count.balance) - float(current_leave_count.taken),2)
								current_leave_count.save()


								#done: KRIA ATTENDANCE
								createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)							
							# done: CHECK KARIK LEAVE IHA FULAN PRIMEIRU
							else:
								print('ANOTHER CALL 1')
								current_leave_count.taken = round(float(current_leave_count.taken) + days,2)
								if check_last_period:
									print('ANOTHER CALL 2')
									current_leave_count.total_earn = round(float(last_count_period.total_balance) + float(earn_per_month),1)
									current_leave_count.balance = round(float(last_count_period.total_balance) + float(earn_per_month) - float(current_leave_count.taken),2 )
									current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
									current_leave_count.balance_month = round(float(current_leave_count.total_balance) - float(current_leave_count.taken),2)
									current_leave_count.save()
								else:
									print('ANOTHER CALL 3')
									current_leave_count.total_taken = current_leave_count.taken
									current_leave_count.balance = round(float(current_leave_count.leave_earn) - float(current_leave_count.taken),2 )
									current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
									current_leave_count.balance_month = round(float(current_leave_count.balance) - float(current_leave_count.taken),2)
									current_leave_count.save()

								# done: KRIA ATTENDANCE
								createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)


							i = 0
							# done: UPDATE LEAVE RECORD
							while i < len(months):
								m = months[i]
								if i == int(0):
									# work: First Month
									if check_last_period:
										print('PRINT CALL UPDATE CHEK LAST PERIOD')
										first_leave_count = LeaveCount.objects.filter(employee=employee,month__code=m.month, year__year=m.year, period=leave_period,leave_type=leave_type).first()
										first_leave_count.balance = round(float(last_count_period.total_balance) + float(earn_per_month) -  float(first_leave_count.taken),2)
										first_leave_count.total_earn = round(float(first_leave_count.leave_earn) + float(last_count_period.total_balance),2)
										first_leave_count.total_balance = round(float(first_leave_count.total_earn) - float(first_leave_count.total_taken),2)
										first_leave_count.balance_carry = first_leave_count.total_balance
										first_leave_count.total_balance_leave = float(leave_type.total) - float(first_leave_count.total_balance)
										first_leave_count.prov_total_earn = first_leave_count.total_earn
										first_leave_count.balance_month = round(float(first_leave_count.balance) - float(first_leave_count.taken),2)
										first_leave_count.save()
										print('PRINT CALL UPDATE CHEK LAST PERIOD ---- NOT')
									else:
										first_leave_count = LeaveCount.objects.filter(employee=employee,month__code=m.month, year__year=m.year, period=leave_period,leave_type=leave_type).first()
										first_leave_count.balance = round(float(first_leave_count.leave_earn) - float(first_leave_count.taken),2)
										first_leave_count.total_earn = round(float(first_leave_count.leave_earn),2)
										first_leave_count.total_balance = round(float(first_leave_count.balance),2)
										first_leave_count.balance_carry = first_leave_count.total_balance
										first_leave_count.total_balance_leave = float(leave_type.total) - float(first_leave_count.total_balance)
										first_leave_count.prov_total_earn = first_leave_count.leave_earn
										first_leave_count.balance_month = round(float(first_leave_count.balance) - float(first_leave_count.taken),2)
										first_leave_count.save()

								else:
									# work: Next Month
									prev_mont = m.asfreq("M", "S") - 1
									lccurrent = get_object_or_404(LeaveCount, employee=employee, period=leave_period, leave_type=leave_type,  year__year=m.year, month__code=m.month)
									lclast = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type,  year__year=prev_mont.year, month__code=prev_mont.month).first()


									lccurrent.balance = round(float(lclast.balance) + float(lccurrent.leave_earn) - float(lccurrent.taken),2)
									lccurrent.total_earn = round(float(lclast.prov_total_earn) + float(lccurrent.leave_earn),1)
									lccurrent.total_taken = round(float(lclast.total_taken) + float(lccurrent.taken),2)
									lccurrent.total_balance = round(float(lccurrent.total_earn) - float(lccurrent.total_taken),1)
									lccurrent.balance_carry = lccurrent.total_balance
									lccurrent.total_balance_leave = float(leave_type.total) - float(lccurrent.total_balance)
									lccurrent.prov_total_earn = float(lclast.prov_total_earn) + float(earn_per_month)
									lccurrent.balance_month = round(float(lclast.balance) - float(lccurrent.taken),2)
									lccurrent.save()

								i+=1

							# done: KRIA LEAVE
							instance = form.save(commit=False)
							createLeave(request, instance,newid,new_hashid, employee, leave_period)
							messages.success(request, 'Leave Aumenta ho Susesu')
							return redirect('leave-hr-leave-record', c_emp.hashed)

						# done: CHECK KARIK LEAVE LAOS ANNUAL LEAVE
						else:

							lcount = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type, month__isnull=False)
							getmonth = get_object_or_404(Mnth, code=start_date.month)
							getyear = get_object_or_404(Yr, year=start_date.year)

							# done: CHECK LEAVE COUNT NEBE IHA ONA MAIBE FULAN LAIHA
							if lcount:
								previous_leave_count = LeaveCount.objects.filter(period=leave_period, employee=employee,leave_type=leave_type).last()
								month_leave_count = LeaveCount.objects.filter(period=leave_period, employee=employee,leave_type= leave_type, month__code=start_date.month, year__year=start_date.year).last()
								# work: Leave Nebe Iha ona
								if days <= previous_leave_count.total_balance:
									if month_leave_count:
										month_leave_count.taken = round(float(month_leave_count.taken) + days, 2)
										month_leave_count.total_taken = round(float(previous_leave_count.total_taken) +  days,2)
										print(month_leave_count.taken)
										# month_leave_count.total_taken = month_leave_count.taken
										print(month_leave_count.total_taken)
										month_leave_count.total_balance = round(float(leave_type.total) - float(month_leave_count.total_taken),2)
										print(month_leave_count.total_balance)
										month_leave_count.save()
										instance = form.save(commit=False)
										createLeave(request, instance,newid,new_hashid, employee, leave_period)
										createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)
										messages.success(request, 'Leave Aumenta ho Susesu')
										return redirect('leave-hr-leave-record', c_emp.hashed)
									else:
										lc = LeaveCount.objects.create(
											period = leave_period,
											employee = employee,
											leave_type = leave_type,
											year = getyear,
											month = getmonth

										)
										lc.taken = days
										lc.total_taken = round(float(previous_leave_count.total_taken) + float(lc.taken),2)
										lc.total_balance = round(float(leave_type.total) - float(lc.total_taken),2)
										lc.save()
										instance = form.save(commit=False)

										createLeave(request, instance,newid,new_hashid, employee, leave_period)
										createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)

										messages.success(request, 'Leave Aumenta ho Susesu')
										return redirect('leave-hr-leave-record', c_emp.hashed)
								else:
									messages.error(request, 'Loron nebe hili barak liu. Halo favor altera loron nebe ita prienche')
							# done: CHECK LEAVE COUNT NEBE IHA NO FULAN ONA IHA
							else:
								lcount2 = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type)
								lcount2.update(
									month=getmonth,
									year=getyear,
									taken = days,
									total_taken = days,
									total_balance = round(float(leave_type.total) - float(days),2)
								)
								instance = form.save(commit=False)
								createLeave(request, instance,newid,new_hashid, employee, leave_period)

								# KRIA ATTENDANCE
								createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)

								messages.success(request, 'Leave Aumenta ho Susesu')
								return redirect('leave-hr-leave-record', c_emp.hashed)
						
					# done: ERROR KARIK DATA HAHU LAIHA PERIODE NIA LARAN
					else:
						messages.error(request,'Data hahu laiha periode ida ne nia laran!!')
				else:
					messages.error(request,'Total loron nebe ita prienche latuir formato!!')
			else:
				messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
			
	else:
		form = HRLeaveForm()
	context = {
		'group': group, 'c_emp': c_emp,  'page': 'record',
		'form': form, 'emp':emp,
		'title': 'Aplika Licensa', 'legend': 'Aplika Licensa'
	}
	return render(request, 'leave/form.html', context)

# work: Work Here
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeavePeriodAdd(request):
	group = request.user.groups.all()[0].name
	employee = Employee.objects.filter(status_id=1)
	
	if request.method == 'POST':
		form = HRPeriodForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			start_year = form.cleaned_data.get('start_year')
			end_year = form.cleaned_data.get('end_year')
			if start_year.year == end_year.year:
				messages.error(request, "Tinan Hahu ho Tinan Remata labele hanesan tinan remata !")
			else:
				for emp in employee:
					contract = Contract.objects.filter(employee=emp, is_active=True).last()
					allleavep = LeavePeriod.objects.filter(employee=emp)
					for obj in allleavep:
						obj.is_active = False
						obj.save()
					# instance.is_active = True
					# instance.employee = emp
					date_string = f'{start_year}-{contract.start_date.month}-{contract.start_date.day}'
					start_period = dt.strptime(date_string, "%Y-%m-%d").date()
					next_year = pd.date_range(start=start_period, end=start_period+pd.DateOffset(years=1), freq='M')
					end_period = next_year.max()
					# instance.start_month = get_object_or_404(Mnth, code=start_period.month)
					# instance.end_month = get_object_or_404(Mnth, code=end_period.month)
					# instance.start_year = get_object_or_404(Yr, year=start_period.year)
					# instance.end_year = get_object_or_404(Yr, year=end_period.year)
					# instance.start_date = start_period
					# instance.end_date = end_period
					# instance.save()
					LeavePeriod.objects.create(
						employee=emp, \
						start_month = get_object_or_404(Mnth, code=start_period.month),\
						end_month = get_object_or_404(Mnth, code=end_period.month), \
						start_year = get_object_or_404(Yr, year=start_period.year), \
						end_year = get_object_or_404(Yr, year=end_period.year), \
						start_date = start_period,\
						end_date = end_period,\
						is_active = True
					)
				messages.success(request, 'Susesu Aumenta Periode Licensa')
				return redirect('leave-hr-app-raw-list')
					



					# if contract:
					# else:
					# 	messages.error(request, f'Funsrionario/a {emp} seidauk iha Kontrato')
					# 	return redirect('leave-hr-app-raw-list')
	else: form = HRPeriodForm()
	context = {
		'group': group,  'form':form,
		'title': 'Set Period Leave', 'legend': 'Set Period Leave'
	}
	return render(request, 'leave/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveEmpPeriodAdd(request, hashid):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	contract = Contract.objects.filter(employee=employee, is_active=True).last()
	if request.method == 'POST':
		form = HRPeriodForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			start_year = form.cleaned_data.get('start_year')
			end_year = form.cleaned_data.get('end_year')
			if start_year == end_year:
				messages.error(request, "Tinan Hahu ho Tinan Remata labele hanesan")
			else:
				allleavep = LeavePeriod.objects.filter(employee=employee)
				for obj in allleavep:
					obj.is_active = False
					obj.save()
				instance.is_active = True
				instance.employee = employee
				date_string = f'{start_year}-{contract.start_date.month}-{contract.start_date.day}'
				start_period = dt.strptime(date_string, "%Y-%m-%d").date()
				next_year = pd.date_range(start=start_period, end=start_period+pd.DateOffset(years=1), freq='M')
				end_period = next_year.max()
				instance.start_month = get_object_or_404(Mnth, code=start_period.month)
				instance.end_month = get_object_or_404(Mnth, code=end_period.month)
				instance.start_year = get_object_or_404(Yr, year=start_period.year)
				instance.end_year = get_object_or_404(Yr, year=end_period.year)
				instance.start_date = start_period
				instance.end_date = end_period
				instance.save()
				messages.success(request, 'Susesu Aumenta Periode Licensa')
				return redirect('leave-hr-leave-record', hashid)
	else: form = HRPeriodForm()
	context = {
		'group': group, 'form':form, 'page': 'add-emp-record', 'hashid': hashid,
		'title': 'Set Period Leave', 'legend': 'Set Period Leave'
	}
	return render(request, 'leave/form2.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveEmpUpdatePeriodMonth(request, hashid):
	today = dt.today().date()
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	lt = get_object_or_404(LeaveType, pk=1)
	leave_period = LeavePeriod.objects.filter(is_active=True, employee=employee).last()
	leave_count_last = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type_id=1).last()
	get_m = get_object_or_404(Mnth, code=today.month)
	get_y = get_object_or_404(Yr, year=today.year)
	if leave_count_last:
		earn_per_month = round(float(lt.total/12),2)

		lcnew = LeaveCount.objects.create(
			period = leave_period,
			employee=employee,
			leave_type=lt,
			month = get_m,
			year = get_y,
			leave_earn = earn_per_month
		)
		# lc.balance = round(float(lc.leave_earn) - float(lc.taken),2)
		# lc.total_earn = round(float(lc.leave_earn) + float(leave_count_last.total_balance),2)
		# lc.total_balance = round(float(lc.total_earn) - float(lc.total_taken),2)
		# lc.balance_carry = lc.total_balance
		# lc.total_balance_leave = float(lt.total) - float(lc.total_balance)
		# lc.prov_total_earn = lc.total_earn
		# lc.save()
		# lc.taken = round(float(lc.taken) + days,2)
		# lc.total_taken = round(float(leave_count_last.taken) + days)
		# lc.balance = round(float(leave_count_last.balance) + float(lc.leave_earn) - float(days),2 )
		# lc.total_balance = round(float(lc.total_earn) - float(lc.total_taken),1)
		# lc.save()
		lcnew.balance = round(float(leave_count_last.balance) + float(lcnew.leave_earn) - float(lcnew.taken),2)
		lcnew.total_earn = round(float(leave_count_last.prov_total_earn) + float(lcnew.leave_earn),1)
		lcnew.total_balance = round(float(lcnew.total_earn) - float(lcnew.total_taken),1)
		lcnew.balance_carry = lcnew.total_balance
		lcnew.total_balance_leave = float(lt.total) - float(lcnew.total_balance)
		lcnew.prov_total_earn = float(leave_count_last.prov_total_earn) + float(earn_per_month)
		lcnew.save()
	# previous_leave_count = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type_id=1, month__code__lt=start_date.month, year__year=current_leave_count.year.year).last()
		messages.success(request, 'Susesu kria Record iha fulan ida ne')
		return redirect('leave-hr-leave-record', hashid)
	else:
		messages.error(request, 'Deskulpa Laiha Licensa iha Fulan kotuk')
		return redirect('leave-hr-leave-record', hashid)



@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrLeaveUpdateAttBack(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	emp = leave.employee
	per = pd.date_range(start=leave.start_date, end=leave.end_date, freq='B')
	if leave.leave_type.pk == 1:
		attstatus = get_object_or_404(AttendanceStatus, pk=6)
	elif leave.leave_type.pk == 2:
		attstatus = get_object_or_404(AttendanceStatus, pk=3)
	elif leave.leave_type.pk == 3:
		attstatus = get_object_or_404(AttendanceStatus, pk=12)
	elif leave.leave_type.pk == 4:
		attstatus = get_object_or_404(AttendanceStatus, pk=7)
	elif leave.leave_type.pk == 5:
		attstatus = get_object_or_404(AttendanceStatus, pk=8)
	for i in per:
		newid, hashedid = getnewid(Attendance)
		y = leave.start_date.year
		m = leave.start_date.month
		year = get_object_or_404(Year, year=y)
		month = get_object_or_404(Month, pk=m)
		created = Attendance.objects.create(
		id = newid,
		unit = emp.curempdivision.unit,
		employee = emp,
		year = year,
		month = month,
		date = i,
		status_am = attstatus,
		status_pm = attstatus,
		datetime=timezone.now(),
		user=request.user,
		hashed = hashedid)
		leave.is_update = True
		leave.save()


	messages.success(request, 'Susesu Altera')
	return redirect('leave-hr-app-detail', hashid)
@login_required
@allowed_users(allowed_roles=['hr','hr_s'])
def hrLeaveUpdateAtt(request, hashid, hashid2):
	group = request.user.groups.all()[0].name
	employee = get_object_or_404(Employee, hashed=hashid)
	leave_period = LeavePeriod.objects.filter(employee=employee,is_active=True).last()
	check_last_period = LeavePeriod.objects.filter(employee=employee, is_active=True, pk__lt=leave_period.pk).last()
	last_count_period = LeaveCount.objects.filter(employee=employee, period=check_last_period, leave_type_id=1).last()
	min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
	max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
	months = pd.period_range(min_month, max_month, freq='M')
	leave = get_object_or_404(Leave, hashed=hashid2)
	c_emp = employee
	newid, new_hashid = getnewid(Leave)
	newsid2, _ = getnewid(LeaveCount)


	leave_type = leave.leave_type
	days = leave.days
	days = round(float(days),2)

	if leave_type.pk == 1: earn_per_month = round(float(leave_type.total/12),2)
	else: earn_per_month = 0.00

	start_date = leave.start_date
	end_date = leave.end_date
	last_two_digits = str(days).split('.')[1][:2]
	last_two_digits = int(last_two_digits)

	min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
	max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
	date1 = pd.to_datetime(start_date, format="%Y %m").date()

	start_date_period = pd.to_datetime(min_month, format="%Y %m").date()
	end_date_period = pd.to_datetime(max_month, format="%Y %m").date()
	start_month = date1


	if days <= leave_type.total:
		# done: CHECK ANGKA LORON 0.5/1.0/1.5
		if last_two_digits == int(5) or last_two_digits == int(0):
			# done: CHECK DATA LEAVE IHA PERIODO NIA LARAN
			if start_date_period <= start_month <= end_date_period + datetime.timedelta(days=29):
				# done: CHECK LEAVE TYPE BA ANNUAL
				if leave_type.pk == 1:
					# done: CHECK RECORD IHA FULAN IDA NE'E
					current_leave_count = get_object_or_404(LeaveCount, period=leave_period, employee=employee,leave_type= leave_type, month__code=start_date.month, year__year=start_date.year)
					previous_leave_count = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type= leave_type, month__code__lt=start_date.month, year__year=current_leave_count.year.year).last()
					# done: CHECK KARIK LEAVE IHA FULAN KLARAN
					if previous_leave_count:
						current_leave_count.taken = round(float(current_leave_count.taken) + days,2)
						current_leave_count.total_taken = round(float(previous_leave_count.taken) + days)
						current_leave_count.balance = round(float(previous_leave_count.balance) + float(current_leave_count.leave_earn) - float(days),2 )
						current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
						current_leave_count.balance_month = round(float(previous_leave_count.balance) - float(current_leave_count.taken),2)
						current_leave_count.save()


						#done: KRIA ATTENDANCE
						createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)							
					# done: CHECK KARIK LEAVE IHA FULAN PRIMEIRU
					else:
						current_leave_count.taken = round(float(current_leave_count.taken) + days,2)
						current_leave_count.total_taken = current_leave_count.taken
						current_leave_count.balance = round(float(current_leave_count.leave_earn) - float(current_leave_count.taken),2 )
						current_leave_count.total_balance = round(float(current_leave_count.total_earn) - float(current_leave_count.total_taken),1)
						current_leave_count.balance_month = round(float(current_leave_count.balance) - float(current_leave_count.taken),2)
						current_leave_count.save()

						# done: KRIA ATTENDANCE
						createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)


					i = 0
					# done: UPDATE LEAVE RECORD
					while i < len(months):
						m = months[i]
						if i == int(0):
							# done: FULAN PRIMEIRO
							if check_last_period:
								first_leave_count = LeaveCount.objects.filter(employee=employee,month__code=m.month, year__year=m.year, period=leave_period,leave_type=leave_type).first()
								first_leave_count.balance = round(float(first_leave_count.leave_earn) - float(first_leave_count.taken),2)
								first_leave_count.total_earn = round(float(first_leave_count.leave_earn) + float(last_count_period.total_balance),2)
								first_leave_count.total_balance = round(float(first_leave_count.total_earn) - float(first_leave_count.total_taken),2)
								first_leave_count.balance_carry = first_leave_count.total_balance
								first_leave_count.total_balance_leave = float(leave_type.total) - float(first_leave_count.total_balance)
								first_leave_count.prov_total_earn = first_leave_count.total_earn
								first_leave_count.balance_month = round(float(first_leave_count.balance) - float(first_leave_count.taken),2)
								first_leave_count.save()
							else:
								first_leave_count = LeaveCount.objects.filter(employee=employee,month__code=m.month, year__year=m.year, period=leave_period,leave_type=leave_type).first()
								first_leave_count.balance = round(float(first_leave_count.leave_earn) - float(first_leave_count.taken),2)
								first_leave_count.total_earn = round(float(first_leave_count.leave_earn),2)
								first_leave_count.total_balance = round(float(first_leave_count.balance),2)
								first_leave_count.balance_carry = first_leave_count.total_balance
								first_leave_count.total_balance_leave = float(leave_type.total) - float(first_leave_count.total_balance)
								first_leave_count.prov_total_earn = first_leave_count.leave_earn
								first_leave_count.balance_month = round(float(first_leave_count.balance) - float(first_leave_count.taken),2)
								first_leave_count.save()

						else:
							# done: FULAN TUIR MAI
							prev_mont = m.asfreq("M", "S") - 1
							lccurrent = get_object_or_404(LeaveCount, employee=employee, period=leave_period, leave_type=leave_type,  year__year=m.year, month__code=m.month)
							lclast = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type,  year__year=prev_mont.year, month__code=prev_mont.month).first()


							lccurrent.balance = round(float(lclast.balance) + float(lccurrent.leave_earn) - float(lccurrent.taken),2)
							lccurrent.total_earn = round(float(lclast.prov_total_earn) + float(lccurrent.leave_earn),1)
							lccurrent.total_taken = round(float(lclast.total_taken) + float(lccurrent.taken),2)
							lccurrent.total_balance = round(float(lccurrent.total_earn) - float(lccurrent.total_taken),1)
							lccurrent.balance_carry = lccurrent.total_balance
							lccurrent.total_balance_leave = float(leave_type.total) - float(lccurrent.total_balance)
							lccurrent.prov_total_earn = float(lclast.prov_total_earn) + float(earn_per_month)
							lccurrent.balance_month = round(float(lclast.balance) - float(lccurrent.taken),2)
							lccurrent.save()

						i+=1

					# done: KRIA LEAVE

				# done: CHECK KARIK LEAVE LAOS ANNUAL LEAVE
				else:

					lcount = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type, month__isnull=False)
					getmonth = get_object_or_404(Mnth, code=start_date.month)
					getyear = get_object_or_404(Yr, year=start_date.year)

					# done: CHECK LEAVE COUNT NEBE IHA ONA MAIBE FULAN LAIHA
					if lcount:
						previous_leave_count = LeaveCount.objects.filter(period=leave_period, employee=employee,leave_type=leave_type).last()
						month_leave_count = LeaveCount.objects.filter(period=leave_period, employee=employee,leave_type= leave_type, month__code=start_date.month, year__year=start_date.year).last()
						# work: Leave Nebe Iha ona
						if days <= previous_leave_count.total_balance:
							if month_leave_count:
								month_leave_count.taken = round(float(month_leave_count.taken) + days, 2)
								month_leave_count.total_taken = round(float(previous_leave_count.total_taken) +  days,2)
								month_leave_count.total_balance = round(float(leave_type.total) - float(month_leave_count.total_taken),2)
								month_leave_count.save()
								createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)
								messages.success(request, 'Susesu Altera')
								return redirect('leave-hr-app-detail', hashid2)
							else:
								lc = LeaveCount.objects.create(
									period = leave_period,
									employee = employee,
									leave_type = leave_type,
									year = getyear,
									month = getmonth

								)
								lc.taken = days
								lc.total_taken = round(float(previous_leave_count.total_taken) + float(lc.taken),2)
								lc.total_balance = round(float(leave_type.total) - float(lc.total_taken),2)
								lc.save()

								createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)

								messages.success(request, 'Susesu Altera')
								return redirect('leave-hr-app-detail', hashid2)
						else:
							messages.error(request, 'Loron nebe hili barak liu. Halo favor altera loron nebe ita prienche')
					# done: CHECK LEAVE COUNT NEBE IHA NO FULAN ONA IHA
					else:
						lcount2 = LeaveCount.objects.filter(employee=employee, period=leave_period, leave_type=leave_type)
						lcount2.update(
							month=getmonth,
							year=getyear,
							taken = days,
							total_taken = days,
							total_balance = round(float(leave_type.total) - float(days),2)
						)

						# KRIA ATTENDANCE
						createAttendance(request, leave_type, Attendance, AttendanceStatus, employee, start_date, end_date, YAten, Maten)

						messages.success(request, 'Susesu Altera')
						return redirect('leave-hr-app-detail', hashid2)
				
			# done: ERROR KARIK DATA HAHU LAIHA PERIODE NIA LARAN
			else:
				messages.error(request,'Data hahu laiha periode ida ne nia laran!!')
		else:
			messages.error(request,'Total loron nebe ita prienche latuir formato!!')
	else:
		messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
	



	leave.hr_confirm = True
	leave.is_done = True
	leave.save()


	messages.success(request, 'Susesu Altera')
	return redirect('leave-hr-app-detail', hashid2)
