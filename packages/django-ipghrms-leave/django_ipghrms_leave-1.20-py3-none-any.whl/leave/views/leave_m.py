import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import employee
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision, Employee
from leave.models import Leave, LeaveCount, LeaveDelegate, LeaveUnit, LeaveDep, LeavePeriod
from leave.forms import LeaveDelegateForm2, LeaveForm, LeaveDelegateForm1, LeaveCancelForm
from contract.models import EmpPosition
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff, c_unit, c_dep
from datetime import datetime as dt
import pandas as pd
from leave.utils import calculate_days, koko
from django.db.models import Q
from leave.utils import count_day
from log.utils import log_action
from leave.utils_2 import koko2, calculate_leave_days
@login_required
def LeaveAdd(request):
	group = request.user.groups.all()[0].name
	c_emp = []
	if group == "staff":
		c_emp = c_staff(request.user)
	elif group == "unit":
		c_emp, _ = c_unit(request.user)
	else:
		c_emp = c_staff(request.user)
	lp = LeavePeriod.objects.filter(employee=c_emp,is_active=True).exists()
	period = LeavePeriod.objects.filter(employee=c_emp,is_active=True).last()
	
	if period :

		empdiv = CurEmpDivision.objects.get(employee=c_emp)
		if lp == True:
			if request.method == 'POST':
				newid, new_hashid = getnewid(Leave)
				form = LeaveForm(request.POST, request.FILES)
				if form.is_valid():
					today = dt.today().date()
					leave_period = LeavePeriod.objects.filter(employee=c_emp,is_active=True).last()
					start_date = form.cleaned_data.get('start_date')
					end_date = form.cleaned_data.get('end_date')
					start_time_status = form.cleaned_data.get('start_time_status')
					end_time_status = form.cleaned_data.get('end_time_status')
					leave_type = form.cleaned_data.get('leave_type')
					start_dt = dt(start_date.year, start_date.month, start_date.day)
					end_dt = dt(end_date.year, end_date.month, end_date.day)
					try:
						days = calculate_leave_days(start_dt, end_dt, start_time_status, end_time_status)
					except ValueError as e:
						messages.warning(request, str(e))
						return render(request, 'leave/form.html', 
		    				{ 
							'message':e, 
							'group': group, 'c_emp': c_emp, 'empdiv': empdiv, 'form': form, 'page': 'apply',
							'title': 'Formulario Aplika Licensa', 'legend': 'Formulario Aplika Licensa'
							}
							)
					days = round(float(days),2)
					last_two_digits = str(days).split('.')[1][:2]
					last_two_digits = int(last_two_digits)

					min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
					max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
					date1 = pd.to_datetime(start_date, format="%Y %m").date()
					date2 = pd.to_datetime(end_date, format="%Y %m").date()

					start_date_period = pd.to_datetime(min_month, format="%Y %m").date()
					end_date_period = pd.to_datetime(max_month, format="%Y %m").date()
					start_month = date1
					# cal_day = count_day(start_date, end_date)

					if start_date_period <= start_month <= end_date_period + datetime.timedelta(days=29):
						if leave_type.pk == 1:
							leave_this_month = LeaveCount.objects.filter(period=leave_period, employee=c_emp, leave_type_id=1, update_date__lte=today).last()
							if leave_this_month.total_balance >= 0.5:
								if   days <= leave_this_month.total_balance or days <= leave_this_month.total_balance + 5 :

									if days < 30  or days >= 30:
										
										if last_two_digits == int(5) or last_two_digits == int(0):
											instance = form.save(commit=False)
											instance.id = newid
											instance.employee = c_emp

											if group == "unit":
												instance.unit_confirm = True
												instance.unit_send = True
											if group == "dep":
												instance.is_lock = True
												instance.is_send = True
											if group == "de":
												instance.is_lock = True
												instance.is_approve = True
												instance.is_finish = True
												instance.is_finish = True
												instance.pr_send = True
												instance.obs = "Sim"
												instance.pr_approve = True
											instance.datetime = datetime.datetime.now()
											instance.user = request.user
											instance.hashed = new_hashid
											instance.leave_period  = period
											instance.leave_type = leave_type
											instance.days = days
											instance.save()
											if group == "unit":
												leaveunit = LeaveUnit.objects.filter(leave_id=newid).first()
												leaveunit.obs = "Sim"
												instance.leave_type = leave_type
												leaveunit.user = request.user
												leaveunit.datetime = datetime.datetime.now()
												leaveunit.save()
											if group == "dep":

												leavedep = LeaveDep.objects.filter(leave_id=newid).first()
												instance.leave_type = leave_type
												leavedep.obs = "Sim"
												leavedep.user = request.user
												leavedep.datetime = datetime.datetime.now()
												leavedep.save()
											
											messages.success(request, f'Aumeta sucessu.')
											if group == "staff" or group == "hr": return redirect('leave-s-detail', hashid=new_hashid)
											if group == "dep": return redirect('leave-dep-detail', hashid=new_hashid)
											elif group == "unit" or group == "deputy": return redirect('leave-c-detail', hashid=new_hashid)
											elif group == "de" : return redirect('leave-de-appr-detail', hashid=new_hashid)
										else:
											messages.error(request,'Total loron nebe ita prienche latuir formato!! Total Loron Nebe Valido: *.00 Sura ba loron  no  *.5 Sura ba "Stengah Hari" ')
									else:
										messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
								else:
									messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
							else:
								messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
						else:
							leave_this_month = LeaveCount.objects.filter(period=leave_period, employee=c_emp, leave_type_id=leave_type.pk).last()
							if leave_this_month.total_balance >= 0.5:
								if   days <= leave_this_month.total_balance or days <= leave_this_month.total_balance + 5 :

									if days < 30  or days >= 30:
										
										if last_two_digits == int(5) or last_two_digits == int(0):
											if float(leave_this_month.total_balance) >= float(days):
												if leave_type.pk != 1:
													# leave_this_month.taken =  days
													# leave_this_month.total_taken = float(leave_this_month.total_taken) + float(days)
													# leave_this_month.total_balance = float(leave_this_month.total_balance) - float(days)
													# leave_this_month.save()
													instance = form.save(commit=False)
													instance.id = newid
													instance.employee = c_emp

												if group == "unit":
													instance.unit_confirm = True
													instance.unit_send = True
												if group == "dep":
													instance.is_lock = True
													instance.is_send = True
												if group == "de":
													instance.is_lock = True
													instance.is_approve = True
													instance.is_finish = True
													instance.is_finish = True
													instance.pr_send = True
													instance.obs = "Sim"
													instance.pr_approve = True
												instance.datetime = datetime.datetime.now()
												instance.user = request.user
												instance.hashed = new_hashid
												instance.leave_period  = period
												instance.leave_type = leave_type
												instance.days = days
												instance.save()
												if group == "unit":
													leaveunit = LeaveUnit.objects.filter(leave_id=newid).first()
													leaveunit.obs = "Sim"
													instance.leave_type = leave_type
													leaveunit.user = request.user
													leaveunit.datetime = datetime.datetime.now()
													leaveunit.save()
												if group == "dep":

													leavedep = LeaveDep.objects.filter(leave_id=newid).first()
													instance.leave_type = leave_type
													leavedep.obs = "Sim"
													leavedep.user = request.user
													leavedep.datetime = datetime.datetime.now()
													leavedep.save()
												
												messages.success(request, f'Aumeta sucessu.')
												if group == "staff" or group == "hr": return redirect('leave-s-detail', hashid=new_hashid)
												if group == "dep": return redirect('leave-dep-detail', hashid=new_hashid)
												elif group == "unit" or group == "deputy": return redirect('leave-c-detail', hashid=new_hashid)
												elif group == "de" : return redirect('leave-de-appr-detail', hashid=new_hashid)
											else:
												messages.error(request,f'Balansu loron la suficiente ona ba tipu licenca {leave_type}'  )
										else:
											messages.error(request,'Total loron nebe ita prienche latuir formato!! Total Loron Nebe Valido: *.00 Sura ba loron  no  *.5 Sura ba "Stengah Hari" ')
									else:
										messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
								else:
									messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
							else:
								messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
					else:
						messages.error(request,'Data hahu laiha periode ida ne nia laran. Halo Favor Kontakto Rekurso Humano hodi Kria Uluk Periode Licensa Foun!')
			else: form = LeaveForm()
		else:
			messages.error(request, 'Periode ba Lisensa seidauk determina')
			if group == "staff": return redirect('leave-s-list')
			if group == "dep": return redirect('leave-dep-list')
			elif group == "unit": return redirect('leave-c-list')
			elif group == "de": return redirect('leave-de-list')
			elif group == "deputy": return redirect('leave-de-list')
			elif group == "hr": return redirect('leave-hr-list')
		context = {
			'group': group, 'c_emp': c_emp, 'empdiv': empdiv, 'form': form, 'page': 'apply',
			'title': 'Formulario Aplika Licensa', 'legend': 'Formulario Aplika Licensa'
		}
		return render(request, 'leave/form.html', context)
	else:
		messages.error(request, 'Periode Licensa seidauk kria. Halo Favor Kontakto Rekurso Humano')
		if group == "staff": return redirect('leave-s-list')
		if group == "dep": return redirect('leave-dep-list')
		elif group == "unit": return redirect('leave-c-list')
		elif group == "de": return redirect('leave-de-list')
		elif group == "deputy": return redirect('leave-de-list')
		elif group == "hr": return redirect('leave-hr-list')


@login_required
def LeaveUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	leave = get_object_or_404(Leave, hashed=hashid)
	c_emp = []
	if group == "staff":
		c_emp = c_staff(request.user)
	elif group == "unit":
		c_emp, _ = c_unit(request.user)
	else:
		c_emp = c_staff(request.user)
	lp = LeavePeriod.objects.filter(employee=c_emp,is_active=True).exists()
	period = LeavePeriod.objects.filter(employee=c_emp,is_active=True).last()
	
	if period :

		empdiv = CurEmpDivision.objects.get(employee=c_emp)
		if lp == True:
			if request.method == 'POST':
				form = LeaveForm(request.POST,  request.FILES, instance=leave)
				if form.is_valid():
					today = dt.today().date()
					leave_period = LeavePeriod.objects.filter(employee=c_emp,is_active=True).last()
					start_date = form.cleaned_data.get('start_date')
					end_date = form.cleaned_data.get('end_date')
					start_time_status = form.cleaned_data.get('start_time_status')
					end_time_status = form.cleaned_data.get('end_time_status')

					start_dt = dt(start_date.year, start_date.month, start_date.day)
					end_dt = dt(end_date.year, end_date.month, end_date.day)
					try:
						days = calculate_leave_days(start_dt, end_dt, start_time_status, end_time_status)
					except ValueError as e:
						messages.warning(request, str(e))
						return render(request, 'leave/form.html', 
		    				{ 
							'message':e, 
							'group': group, 'c_emp': c_emp, 'empdiv': empdiv, 'form': form, 'page': 'apply',
							'title': 'Formulario Aplika Licensa', 'legend': 'Formulario Aplika Licensa'
							}
							)
					days = round(float(days),2)
					last_two_digits = str(days).split('.')[1][:2]
					last_two_digits = int(last_two_digits)

					min_month = f'{leave_period.start_year.year}-{leave_period.start_month.code}'
					max_month = f'{leave_period.end_year.year}-{leave_period.end_month.code}'
					date1 = pd.to_datetime(start_date, format="%Y %m").date()
					date2 = pd.to_datetime(end_date, format="%Y %m").date()

					start_date_period = pd.to_datetime(min_month, format="%Y %m").date()
					end_date_period = pd.to_datetime(max_month, format="%Y %m").date()
					start_month = date1
					# cal_day = count_day(start_date, end_date)

					if start_date_period <= start_month <= end_date_period + datetime.timedelta(days=29):
						
						leave_this_month = LeaveCount.objects.filter(period=leave_period, employee=c_emp, leave_type_id=1, update_date__lte=today).last()
						if leave_this_month.balance >= 0.5:
							if   days <= leave_this_month.balance or days <= leave_this_month.balance + 5 :

								if days < 30  or days >= 30:
									
									if last_two_digits == int(5) or last_two_digits == int(0):
										instance = form.save(commit=False)
										instance.employee = c_emp
										if group == "unit":
											instance.unit_confirm = True
											instance.unit_send = True
										if group == "dep":
											instance.is_lock = True
											instance.is_send = True
										if group == "de":
											instance.is_lock = True
											instance.is_approve = True
											instance.is_finish = True
											instance.is_finish = True
											instance.pr_send = True
											instance.obs = "Sim"
											instance.pr_approve = True
										instance.datetime = datetime.datetime.now()
										instance.user = request.user
										instance.leave_period  = period
										instance.days = days
										instance.save()
										if group == "unit":
											leaveunit = LeaveUnit.objects.filter(leave_id=leave.pk).first()
											leaveunit.obs = "Sim"
											leaveunit.user = request.user
											leaveunit.datetime = datetime.datetime.now()
											leaveunit.save()
										if group == "dep":

											leavedep = LeaveDep.objects.filter(leave_id=leave.pk).first()
											leavedep.obs = "Sim"
											leavedep.user = request.user
											leavedep.datetime = datetime.datetime.now()
											leavedep.save()
										
										messages.success(request, f'Aumeta sucessu.')
										if group == "staff" or group == "hr": return redirect('leave-s-detail', hashid=hashid)
										if group == "dep": return redirect('leave-dep-detail', hashid=hashid)
										elif group == "unit" or group == "deputy": return redirect('leave-c-detail', hashid=hashid)
										elif group == "de" : return redirect('leave-de-appr-detail', hashid=hashid)
									else:
										messages.error(request,'Total loron nebe ita prienche latuir formato!! Total Loron Nebe Valido: *.00 Sura ba loron  no  *.5 Sura ba "Stengah Hari" ')
								else:
									messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
							else:
								messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
						else:
							messages.error(request, f'Loron nebe hili barak liu. Halo favor hare regulamentu konaba total licenca.')
					else:
						messages.error(request,'Data hahu laiha periode ida ne nia laran. Halo Favor Kontakto Rekurso Humano hodi Kria Uluk Periode Licensa Foun!')
			else: form = LeaveForm(instance=leave)
		else:
			messages.error(request, 'Periode ba Lisensa seidauk determina')
			if group == "staff": return redirect('leave-s-list')
			if group == "dep": return redirect('leave-dep-list')
			elif group == "unit": return redirect('leave-c-list')
			elif group == "de": return redirect('leave-de-list')
			elif group == "deputy": return redirect('leave-de-list')
			elif group == "hr": return redirect('leave-hr-list')
		context = {
			'group': group, 'c_emp': c_emp, 'empdiv': empdiv, 'form': form, 'page': 'apply',
			'title': 'Formulario Aplika Licensa', 'legend': 'Formulario Aplika Licensa'
		}
		return render(request, 'leave/form.html', context)
	else:
		messages.error(request, 'Periode Licensa seidauk kria. Halo Favor Kontakto Rekurso Humano')
		if group == "staff": return redirect('leave-s-list')
		if group == "dep": return redirect('leave-dep-list')
		elif group == "unit": return redirect('leave-c-list')
		elif group == "de": return redirect('leave-de-list')
		elif group == "deputy": return redirect('leave-de-list')
		elif group == "hr": return redirect('leave-hr-list')


# @login_required
# def LeaveUpdate(request, hashid):
# 	group = request.user.groups.all()[0].name
# 	c_emp = c_staff(request.user)
# 	empdiv = CurEmpDivision.objects.get(employee=c_emp)
# 	objects = get_object_or_404(Leave, hashed=hashid)
# 	if request.method == 'POST':
# 		form = LeaveForm(request.POST,request.FILES, instance=objects)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.save()
# 			log_action(request, model=Leave._meta.model_name, action="Update",field_id=objects.pk)
# 			messages.success(request, f'Altera sucessu.')
# 			if group == "staff": return redirect('leave-s-detail', hashid=hashid)
# 			elif group == "hr": return redirect('leave-s-detail', hashid=hashid)
# 			elif group == "unit": return redirect('leave-c-detail', hashid=hashid)
# 	else: form = LeaveForm(instance=objects)
# 	context = {
# 		'group': group, 'c_emp': c_emp, 'empdiv': empdiv, 'form': form, 'page': 'apply',
# 		'title': 'Altera Aplikasaun', 'legend': 'Altera Aplikasaun'
# 	}
# 	return render(request, 'leave/form.html', context)

@login_required
def LeaveLock(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	objects.is_lock =  True
	objects.save()
	messages.success(request, f'Xavi.')
	if group == "staff": return redirect('leave-s-detail', hashid=hashid)
	elif group == "hr": return redirect('leave-s-detail', hashid=hashid)
	elif group == "unit": return redirect('leave-c-detail', hashid=hashid)
	elif group == "deputy": return redirect('leave-c-detail', hashid=hashid)

@login_required
def LeaveUnLock(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	objects.is_lock =  False
	objects.save()
	messages.success(request, f'Loke.')
	if group == "staff": return redirect('leave-s-detail', hashid=hashid)
	elif group == "hr": return redirect('leave-s-detail', hashid=hashid)
	elif group == "unit": return redirect('leave-c-detail', hashid=hashid)
	elif group == "deputy": return redirect('leave-c-detail', hashid=hashid)

@login_required
def LeaveSend(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	if group == "staff" or group == "hr":
		check_ekipa = EmpPosition.objects.filter(Q(department__isnull=False)&Q(department=empdiv.department), is_active=True, is_manager=True).exists()
		check_div = EmpPosition.objects.filter(Q(unit__isnull=False)&Q(unit=empdiv.unit), is_active=True).exists()
		if check_ekipa and check_div or check_ekipa:
			objects.is_send =  True
			objects.is_finish =  False
			objects.save()
			messages.success(request, f'Manda ona.')
		elif check_div:
			objects.is_send_to_div =  True
			objects.is_finish =  False
			objects.save()
			messages.success(request, f'Manda ona.')
		else:
			messages.error(request, "Funsionario Refere Laiha Chefe Ekipa no Chefe Divizaun, Halo favor kontakto Rekurso Humano")
		if group == "staff": return redirect('leave-s-detail', hashid=hashid)
		elif group == "hr": return redirect('leave-s-detail', hashid=hashid)
		elif group == "unit": return redirect('leave-c-detail', hashid=hashid)

@login_required
def LeaveUnitSend(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	if group == 'unit':
		objects.unit_send_pr =  True
	if group == 'deputy':
		objects.unit_send_pr =  True
	objects.is_finish =  False
	objects.save()
	messages.success(request, f'Manda ona ba Presidente')
	return redirect('leave-c-detail', hashid=hashid)

@login_required
def LeaveUnitDone(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(Leave, hashed=hashid)
	objects.is_done =  True
	objects.save()
	messages.success(request, f'Susesi Termina Licensa')
	return redirect('leave-c-detail', hashid=hashid)

@login_required
def LeaveDelegUpdate(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	leave = get_object_or_404(Leave, hashed=hashid)
	objects = LeaveDelegate.objects.get(leave=leave)
	if request.method == 'POST':
		form = LeaveDelegateForm1(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			if group == "staff": return redirect('leave-s-detail', hashid=hashid)
			elif group == "unit": return redirect('leave-c-detail', hashid=hashid)
	else: form = LeaveDelegateForm1(instance=objects)
	context = {
		'c_emp': c_emp, 'empdiv': empdiv, 'leave': leave, 'form': form, 'page': 'delegate',
		'title': 'Delega ba', 'legend': 'Delega ba'
	}
	return render(request, 'leave/form.html', context)
###
@login_required
def LeaveDelegConfirm(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	objects = get_object_or_404(LeaveDelegate, hashed=hashid)
	leave = objects.leave
	if request.method == 'POST':
		form = LeaveDelegateForm2(request.POST, instance=objects)
		if form.is_valid():
			obs = form.cleaned_data.get('obs')
			instance = form.save(commit=False)
			instance.is_confirm = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumeta sucessu.')
			return redirect('leave-deleg-detail', hashid=hashid)
	else: form = LeaveDelegateForm2(instance=objects)
	context = {
		'c_emp': c_emp, 'empdiv': empdiv, 'leave': objects.leave, 'form': form, 'page': 'delegate',
		'title': 'Konsiente ba Delegasaun Servisu', 'legend': 'Konsiente ba Delegasaun Servisu'
	}
	return render(request, 'leave/form.html', context)

@login_required
def LeaveDelegConfirm2(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(LeaveDelegate, hashed=hashid)
	if objects.obs == 'Sim':
		objects.is_confirm2 =  True
	objects.save()
	leave = objects.leave
	leave.is_delegate = True
	if objects.obs == 'Lae':
		leave.is_send = False
	leave.save()
	messages.success(request, f'Konfirma ona.')
	return redirect('leave-deleg-detail', hashid=hashid)

@login_required
def LeaveDelegCancel(request, hashid):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(LeaveDelegate, hashed=hashid)
	objects.is_confirm =  False
	objects.is_confirm2 =  False
	objects.save()
	messages.success(request, f'Konfirmasaun cancela.')
	return redirect('leave-deleg-detail', hashid=hashid)


@login_required
def LeaveCancel(request, hashid):
	group = request.user.groups.all()[0].name
	c_emp = c_staff(request.user)
	empdiv = CurEmpDivision.objects.get(employee=c_emp)
	objects = get_object_or_404(Leave, hashed=hashid)
	if request.method == 'POST':
		form = LeaveCancelForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.cancel_by = request.user
			instance.is_cancel = True
			instance.save()
			messages.success(request, f'Susesu Kansela')
			if group == "staff" or group == "hr": return redirect('leave-s-detail', hashid=hashid)
			if group == "dep": return redirect('leave-dep-detail', hashid=hashid)
			elif group == "unit" or group == "deputy": return redirect('leave-c-detail', hashid=hashid)
			elif group == "de" : return redirect('leave-de-appr-detail', hashid=hashid)
	else: form = LeaveCancelForm(instance=objects)
	context = {
		'c_emp': c_emp, 'empdiv': empdiv, 'leave': objects, 'form': form, 'page': 'kansela',
		'title': 'Kansela Licensa', 'legend': 'Kansela Licensa'
	}
	return render(request, 'leave/form.html', context)

