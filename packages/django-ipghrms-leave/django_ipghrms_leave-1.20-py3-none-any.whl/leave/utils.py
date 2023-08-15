from django.shortcuts import get_object_or_404
from settings_app.utils import getnewid
from django.utils import timezone
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt

def convert_value(value):
    if 0 < value < 10:
        return value / 10
    return value

def check_time_range(start_time, end_time):
    morning_start = "08:00"
    morning_end = "12:00"
    afternoon_start = "14:00"
    afternoon_end = "17:00"
    mor = False
    aft = False
    
    if (morning_start <= start_time <= morning_end) and (morning_start <= end_time <= morning_end):
        mor = True
        aft = False
        return mor, aft
    elif (afternoon_start <= start_time <= afternoon_end) and (afternoon_start <= end_time <= afternoon_end):
        mor = False
        aft = True
        return mor, aft
    else:
        return mor, aft

def calculate_hours(start_time, end_time):
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.strptime(end_time, "%H:%M")
    
    difference = end_datetime - start_datetime
    total_minutes = int(difference.total_seconds() / 60)
    total_hours, remainder_minutes = divmod(total_minutes, 60)
    
    total_time = "{}.{:02d}".format(total_hours, remainder_minutes)
    total = convert_value(float(total_time))
    return round(total,2)



def add_time(t1, t2):
    t1_hour, t1_min = map(int, t1.split(":"))
    t2_hour, t2_min = map(int, t2.split(":"))
    
    total_min = t1_min + t2_min
    total_hour = t1_hour + t2_hour + total_min // 60
    total_min = total_min % 60
    
    return total_hour, total_min

def createAttendance(request, leave_type,  attendance, attStatus, employee, start_date, end_date, YAten, Maten):
    attstatus = None
    if leave_type.pk == 1: attstatus = get_object_or_404(attStatus, pk=6)
    elif leave_type.pk == 2: attstatus = get_object_or_404(attStatus, pk=3)
    elif leave_type.pk == 3: attstatus = get_object_or_404(attStatus, pk=12)
    elif leave_type.pk == 4: attstatus = get_object_or_404(attStatus, pk=7)
    elif leave_type.pk == 5: attstatus = get_object_or_404(attStatus, pk=8)
    elif leave_type.pk == 6: attstatus = get_object_or_404(attStatus, pk=14)
    
    period = pd.date_range(start=start_date, end=end_date, freq='B')
    for i in period:
        attstatusam = None
        attstatuspm = None

        attend = attendance.objects.filter(employee=employee,date=i).last()
        if attend:
            if attend.time_am == None and attend.timeout_am == None or attend.time_am != None and attend.timeout_am == None or attend.time_am == None and attend.timeout_am != None:
                newid3, hashid3 = getnewid(attendance)
                attend.status_am = attstatus
                attend.user = request.user
                attend.save()
            elif attend.time_pm == None and attend.timeout_pm == None or attend.time_pm != None and attend.timeout_pm == None or attend.time_pm == None and attend.timeout_pm != None:
                attend.status_pm = attstatus
                attend.user = request.user
                attend.save()
        else:
            newid3, hashid3 = getnewid(attendance)
            year = start_date.year
            mon = start_date.month
            year = get_object_or_404(YAten, year=year)
            month = get_object_or_404(Maten, code = mon)
            attendance.objects.create(
            id = newid3,
            unit = employee.curempdivision.unit,
            employee = employee,
            year = year,
            month = month,
            date = i,
            status_am = attstatusam,
            status_pm = attstatuspm,
            datetime=timezone.now(),
            user=request.user,
            hashed = hashid3)	


def createAttendanceEmp(request, leave_type,  attendance, attStatus, employee, start_date, end_date, YAten, Maten, leave):
    attstatus = None
    if leave_type.pk == 1: attstatus = get_object_or_404(attStatus, pk=6)
    elif leave_type.pk == 2: attstatus = get_object_or_404(attStatus, pk=3)
    elif leave_type.pk == 3: attstatus = get_object_or_404(attStatus, pk=12)
    elif leave_type.pk == 4: attstatus = get_object_or_404(attStatus, pk=7)
    elif leave_type.pk == 5: attstatus = get_object_or_404(attStatus, pk=8)
    elif leave_type.pk == 6: attstatus = get_object_or_404(attStatus, pk=14)

    period = pd.date_range(start=start_date, end=end_date, freq='B')
    for i in period:
        attstatusam = None
        attstatuspm = None
        tot_period = len(period)
        if tot_period == 1:
            if leave.start_time_status == '08:00' and leave.end_time_status == '12:00':
                attstatusam = attstatus
            elif leave.start_time_status == '13:00' and leave.end_time_status == '17:00':
                attstatuspm = attstatus
            else:
                attstatusam = attstatus
                attstatuspm = attstatus
        elif tot_period > 1:
            if i == period[0]:
                if leave.start_time_status == '08:00':
                    attstatusam = attstatus
                    attstatuspm = attstatus
                elif leave.start_time_status == '13:00':
                    attstatuspm = attstatus
            elif i == period[-1]:
                if leave.end_time_status == '12:00':
                    attstatusam = attstatus
                elif leave.end_time_status == '17:00':
                    attstatusam = attstatus
                    attstatuspm = attstatus
            else:
                attstatusam = attstatus
                attstatuspm = attstatus


        attend = attendance.objects.filter(employee=employee,date=i).last()
        if attend:
            if attend.time_am == None and attend.timeout_am == None or attend.time_am != None and attend.timeout_am == None or attend.time_am == None and attend.timeout_am != None:
                newid3, hashid3 = getnewid(attendance)
                attend.status_am = attstatus
                attend.user = request.user
                attend.save()
            elif attend.time_pm == None and attend.timeout_pm == None or attend.time_pm != None and attend.timeout_pm == None or attend.time_pm == None and attend.timeout_pm != None:
                attend.status_pm = attstatus
                attend.user = request.user
                attend.save()
        else:
            # pass
            newid3, hashid3 = getnewid(attendance)
            year = start_date.year
            mon = start_date.month
            year = get_object_or_404(YAten, year=year)
            month = get_object_or_404(Maten, code = mon)
            attendance.objects.create(
            id = newid3,
            unit = employee.curempdivision.unit,
            employee = employee,
            year = year,
            month = month,
            date = i,
            status_am = attstatusam,
            status_pm = attstatuspm,
            datetime=timezone.now(),
            user=request.user,
            hashed = hashid3)	


def createAttendanceSpecial(request, leave_type,  attendance, attStatus, employee, start_date, end_date, YAten, Maten, start_time, end_time):
    attstatus = None
    if leave_type.pk == 1: attstatus = get_object_or_404(attStatus, pk=6)
    elif leave_type.pk == 2: attstatus = get_object_or_404(attStatus, pk=3)
    elif leave_type.pk == 3: attstatus = get_object_or_404(attStatus, pk=12)
    elif leave_type.pk == 4: attstatus = get_object_or_404(attStatus, pk=7)
    elif leave_type.pk == 5: attstatus = get_object_or_404(attStatus, pk=8)
    elif leave_type.pk == 6: attstatus = get_object_or_404(attStatus, pk=14)
    period = pd.date_range(start=start_date, end=end_date, freq='B')
    for i in period:
        attend = attendance.objects.filter(employee=employee,date=i).last()
        if attend:
            mor, aft = check_time_range(start_time, end_time)
            if mor and aft == False:
                attend.status_am = attstatus
                attend.user = request.user
                attend.save()

            elif mor == False and aft:
                attend.status_pm = attstatus
                attend.user = request.user
                attend.save()
        else:
            mor, aft = check_time_range(start_time, end_time)
            if mor and aft == False:
                newid3, hashid3 = getnewid(attendance)
                year = start_date.year
                mon = start_date.month
                year = get_object_or_404(YAten, year=year)
                month = get_object_or_404(Maten, code = mon)
                attendance.objects.create(
                id = newid3,
                unit = employee.curempdivision.unit,
                employee = employee,
                year = year,
                month = month,
                date = i,
                status_am = attstatus,
                datetime=timezone.now(),
                user=request.user,
                hashed = hashid3)	

            elif mor == False and aft:
                newid3, hashid3 = getnewid(attendance)
                year = start_date.year
                mon = start_date.month
                year = get_object_or_404(YAten, year=year)
                month = get_object_or_404(Maten, code = mon)
                attendance.objects.create(
                id = newid3,
                unit = employee.curempdivision.unit,
                employee = employee,
                year = year,
                month = month,
                date = i,
                status_pm = attstatus,
                datetime=timezone.now(),
                user=request.user,
                hashed = hashid3)	



def createLeave(request, instance, newid, new_hashid, employee, leave_period):
    instance.id = newid
    instance.hashed = new_hashid
    instance.employee = employee
    instance.leave_period = leave_period
    instance.user = request.user
    instance.datetime = timezone.now()
    instance.pr_approve = True
    instance.is_lock = True
    instance.is_send = True
    instance.is_approve = True
    instance.is_finish = True
    instance.hr_confirm = True
    instance.is_done = True
    instance.is_create_by_hr = True
    instance.save()

def createLeaveSpecial(request, instance, newid, new_hashid, employee, leave_period, days):
    instance.id = newid
    instance.hashed = new_hashid
    instance.employee = employee
    instance.leave_period = leave_period
    instance.user = request.user
    instance.days = days
    instance.datetime = timezone.now()
    instance.pr_approve = True
    instance.is_approve = True
    instance.is_finish = True
    instance.hr_confirm = True
    instance.is_done = True
    instance.is_special = True
    instance.is_create_by_hr = True
    instance.save()

def createLeaveProcess(request, instance, newid, new_hashid, employee, leave_period):
    instance.id = newid
    instance.hashed = new_hashid
    instance.employee = employee
    instance.leave_period = leave_period
    instance.user = request.user
    instance.datetime = timezone.now()
    instance.hr_confirm = True
    instance.is_create_by_hr = True
    instance.save()

def check_period_date(period_date):
    check_period = False
    current_date = datetime.now()
    str_date = f"{period_date.year}-{period_date.month}-{period_date.day}"
    input_month = int(str_date.split("-")[1])
    input_day = int(str_date.split("-")[2])

    current_month = current_date.month
    current_day = current_date.day

    if current_month > input_month and (current_month == input_month and current_day >= input_day): 
        check_period = True
    else:
        check_period = False
    return check_period

def check_last_month_period(period_date):
    check_period = False
    current_date = datetime.now()
    str_date = f"{period_date.year}-{period_date.month}-{period_date.day}"
    input_month = int(str_date.split("-")[1])
    input_day = int(str_date.split("-")[2])

    current_month = current_date.month
    current_day = current_date.day

    if current_month > input_month and (current_month == input_month and current_day >= input_day):
        check_period = False
    else:
        check_period = True
    
    return check_period

def check_period_range(period):
    min_month = f'{period.start_year.year}-{period.start_month.code}'
    max_month = f'{period.end_year.year}-{period.end_month.code}'
    months = pd.period_range(min_month, max_month, freq='M')
    return months



def check_day(day, current, last):
    
    return True

def count_day(start_date, end_date):
    current_date = start_date
    weekdays = 0
    while current_date <= end_date:
        if current_date.weekday() < 5: # weekday() returns the day of the week as an integer, where Monday is 0 and Sunday is 6
            weekdays += 1
        current_date += timedelta(days=1)
    return weekdays


import datetime as dt
def calculate_days(start_date, start_time_status, end_date, end_time_status):
    
    # Check if start_date or end_date is on a weekend
    if start_date.weekday() in [5, 6] or end_date.weekday() in [5, 6]:
        raise ValueError("Start Date Or End Date Not On A Weekday")
    
    # Calculate the number of days between start_date and end_date
    days = (end_date - start_date).days + 1  # add 1 day to include start_date
    # Calculate the number of days to exclude (weekends and holidays)
    exclude_days = 0
    for day in range(days):
        current_date = start_date + dt.timedelta(days=day)
        if current_date.weekday() in [5, 6]:  # exclude weekends
            exclude_days += 1
    
    # Calculate the actual number of days
    actual_days = days - exclude_days
    
    # Calculate the number of half days for the first day
    if start_time_status == '08:00':
        half_days_first_day = 0
    elif start_time_status == '13:00':
        half_days_first_day = 0.5
    else:
        raise ValueError("Invalid start time")
    
    # Calculate the number of half days for the last day
    if end_date == start_date:
        if end_time_status == '12:00':
            half_days_last_day = 0.5
        elif end_time_status == '17:00':
            half_days_last_day = 1.0
        else:
            raise ValueError("Invalid end time")
    else:
        if end_time_status == '12:00':
            half_days_last_day = 0
        elif end_time_status == '17:00':
            half_days_last_day = 0.5
        else:
            raise ValueError("Invalid end time")
    
    # Calculate the total number of half days
    half_days_total = half_days_first_day + half_days_last_day
    
    # Calculate the number of full days in between
    full_days_between = actual_days - 2  # exclude the first and last day
    if full_days_between < 0:
        full_days_between = 0
    
    # Calculate the total number of half days for full days between
    half_days_total += full_days_between * 1.0
    
    return half_days_total


def koko():
    start_date = dt.datetime(2023, 3, 14)
    end_date = dt.datetime(2023, 3, 14)
    start_time_status = '13:00'
    end_time_status = '17:00'
    half_days_total = calculate_days(start_date, start_time_status, end_date, end_time_status)
    print('Total: ',half_days_total)