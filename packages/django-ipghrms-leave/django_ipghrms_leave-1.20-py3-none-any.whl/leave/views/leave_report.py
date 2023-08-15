import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision, Employee
from leave.models import Leave, LeaveHR, LeaveUnit, LeaveCount, LeavePeriod, Month as Mnth, Year as Yr, LeaveType
from leave.forms import LeaveHRForm, LeaveUnitForm, LeaveForm, HRLeaveForm, HRPeriodForm, HRLeaveCommentForm
from settings_app.utils import getnewid, f_monthname
from settings_app.user_utils import c_staff, c_unit
from dateutil.parser import parser
from datetime import datetime as dt, timedelta
from attendance.models import Attendance, AttendanceStatus,Year, Month
import pytz
import pandas as pd
from django.db.models import Q, F
from django.utils import timezone
from calendar import mdays
from attendance.models import Attendance, AttendanceStatus, Year as YAten, Month as Maten
from leave.utils import createAttendance, createLeave, check_day
from contract.models import Contract
import calendar
from django.utils.safestring import mark_safe
from custom.models import Unit
import numpy as np
from leave.forms import LeaveFilterForm

def get_years():
    current_year = datetime.datetime.now().year
    return [year for year in range(2012, current_year + 1)]

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveReportDash(request):
    form = LeaveFilterForm(request.GET or None)
    years = get_years()
    months = Mnth.objects.all()
    units = Unit.objects.all()
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    leave_type = LeaveType.objects.all()
    if request.method == 'GET':
        tinan = dt.now().year
        if request.GET.get('tinan') != 0:
            tinan = request.GET.get('tinan')
        else:
            tinan = dt.now().year
        tri = request.GET.get('tri')
        fulan = request.GET.get('fulan')
        unit = request.GET.get('unit')
        filtered_leaves = Leave.objects.all()
        allleave = None
        legend = 'Painel Relatior Licensa'
        title = 'Painel Relatior Licensa'
        data = []

        if tinan or tinan and unit:
            filtered_leaves = filtered_leaves.filter(start_date__year=tinan, hr_confirm=True, is_done=True).count()
            allleave = Leave.objects.filter(start_date__year=tinan, is_active=True,employee__curempdivision__unit_id=unit, hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=tinan, is_active=True,employee__curempdivision__unit_id=unit, hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {tinan} </span>'

        
        context=  {
            'title': legend,'legend': legend, 'data': data,'allleave':allleave,
            'years':years,'trimestral':trimestral, 'months':months, 'units':units, 'year':tinan
        }

        
        return render(request, 'leave_report/dash.html', context)
    context = {
        'title': 'Relatorio Licensa', 'legend': 'Relatorio Licensa',
        'years':years, 'trimestral':trimestral, 'months':months, 'units':units
    }
        
    return render(request, 'leave_report/dash.html', context)



@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveReportDash(request):
    years = get_years()
    months = Mnth.objects.all()
    leave_type = LeaveType.objects.all()
    units = Unit.objects.all()
    tyear = dt.now().year
    data = []
    year_get, month = 0,0
    allleave = None
    error = None
    legend = None
    get_year, get_month, get_tri, get_unit, page = None, None, None, None, None
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    getYear = request.POST.get('tinan')
    getMonth = request.POST.get('fulan')
    getUnit = request.POST.get('unit')
    getTri = request.POST.get('tri')
    datamonth = []

    if request.method == 'POST':

        if getTri != '0' and getMonth != '0':
            legend ='Deskulpa, Fulan No Trimestral labele hili hamutuk'
            error = messages.error(request,'Deskulpa, Fulan No Trimestral labele hili hamutuk')
        # done: DONE
        elif getYear != '0'  and getTri != '0' and getUnit != '0':
            tri = int(getTri)
            tri = int(tri)-1
            tris = trimestral[tri]
            allleave = Leave.objects.filter(start_date__year=int(getYear), start_date__month__gte=tris[2],  start_date__month__lte=tris[3], employee__curempdivision__unit_id=int(getUnit), is_active=True, hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=int(getYear), start_date__month__gte=tris[2],  start_date__month__lte=tris[3], employee__curempdivision__unit_id=int(getUnit), hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            unit_name = get_object_or_404(Unit, pk=int(getUnit))
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(int(getYear))} </span>,   <span class="text-danger"> {tris[1]} </span>, Divizaun  <span class="text-danger"> {unit_name.name} </span>'
            get_year = int(getYear)
            get_tri = int(getTri)
            get_unit = int(getUnit)
            page = 'year-tri-unit'
        # done: DONE
        elif getYear!= '0' and getMonth!= '0' and getUnit!= '0':
            monthname = f_monthname(int(getMonth))
            allleave = Leave.objects.filter(start_date__year=int(getYear),start_date__month=int(getMonth),employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(start_date__year=int(getYear),start_date__month=int(getMonth),leave_type=i,employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            unit_name = get_object_or_404(Unit, pk=int(getUnit))
            start_date = dt(int(getYear), int(getMonth), 1)
            end_date = dt(int(getYear), int(getMonth), calendar.monthrange(int(getYear), int(getMonth))[1])
            delta = timedelta(days=1)
            while start_date <= end_date:
                alleave = Leave.objects.filter(start_date=start_date.date(),employee__curempdivision__unit_id=int(getUnit), hr_confirm=True, is_done=True).count()
                datamonth.append([start_date, alleave])
                start_date += delta
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(getYear)} </span>, Fulan  <span class="text-danger"> {monthname} </span>,  Divizaun  <span class="text-danger"> {unit_name.name} </span>'
            get_year = int(getYear)
            get_month = int(getMonth)
            get_unit = int(getUnit)
            page = 'year-month-unit'
        # done: DONE
        elif getYear != '0' and getTri != '0' :
            tri = int(getTri)
            tri = int(tri)-1
            tris = trimestral[tri]
            allleave = Leave.objects.filter(start_date__year=getYear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3],  is_active=True, hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=getYear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(getYear)} </span>,   <span class="text-danger"> {tris[1]} </span>'
            get_year = int(getYear)
            get_tri = int(getTri)
            page = 'year-tri'
        # done: DONE
        elif getMonth != '0' and getUnit != '0' :
            monthname = f_monthname(int(getMonth))
            allleave = Leave.objects.filter(start_date__year=int(tyear),start_date__month=int(getMonth),employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(start_date__year=int(tyear),start_date__month=int(getMonth),leave_type=i,employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            unit_name = get_object_or_404(Unit, pk=int(getUnit))
            start_date = dt(tyear, int(getMonth), 1)
            end_date = dt(tyear, int(getMonth), calendar.monthrange(tyear, int(getMonth))[1])
            delta = timedelta(days=1)
            while start_date <= end_date:
                alleave = Leave.objects.filter(start_date=start_date.date(),employee__curempdivision__unit_id=int(getUnit), hr_confirm=True, is_done=True).count()
                datamonth.append([start_date, alleave])
                start_date += delta
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(tyear)} </span>, Fulan  <span class="text-danger"> {monthname} </span>,  Divizaun  <span class="text-danger"> {unit_name.name} </span>'
            get_month = int(getMonth)
            get_unit = int(getUnit)
            page = 'month-unit'
        # done: DONE
        elif getYear != '0' and getMonth != '0' :
            monthname = f_monthname(int(getMonth))
            allleave = Leave.objects.filter(start_date__year=int(getYear),start_date__month=int(getMonth), hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=int(getYear), start_date__month=int(getMonth),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            start_date = dt(int(getYear), int(getMonth), 1)
            end_date = dt(int(getYear), int(getMonth), calendar.monthrange(int(getYear), int(getMonth))[1])
            delta = timedelta(days=1)
            while start_date <= end_date:
                alleave = Leave.objects.filter(start_date=start_date.date(), hr_confirm=True, is_done=True).count()
                datamonth.append([start_date, alleave])
                start_date += delta
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(getYear)} </span> fulan <span class="text-danger"> {monthname} </span> '
            get_year = int(getYear)
            get_month = int(getMonth)
            page = 'year-month'
        # done: DONE
        elif getYear != '0' and getUnit != '0' :
            allleave = Leave.objects.filter(start_date__year=int(getYear),employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(start_date__year=int(getYear),leave_type=i,employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            unit_name = get_object_or_404(Unit, pk=int(getUnit))
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(getYear)} </span>,  Divizaun  <span class="text-danger"> {unit_name.name} </span>'
            get_year = int(getYear)
            get_unit = int(getUnit)
            page = 'year-unit'
        # done: DONE
        elif getMonth != '0':
            monthname = f_monthname(int(getMonth))
            allleave = Leave.objects.filter(start_date__year=tyear,start_date__month=int(getMonth), hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, start_date__month=int(getMonth),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            start_date = dt(tyear, int(getMonth), 1)
            end_date = dt(tyear, int(getMonth), calendar.monthrange(tyear, int(getMonth))[1])
            delta = timedelta(days=1)
            while start_date <= end_date:
                alleave = Leave.objects.filter(start_date=start_date.date(), hr_confirm=True, is_done=True).count()
                datamonth.append([start_date, alleave])
                start_date += delta
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {tyear} </span> fulan <span class="text-danger"> {monthname} </span> '
            get_month = int(getMonth)
            page = 'month'

        # done: DONE
        elif getTri != '0':
            tri = int(getTri)
            tri = int(tri)-1
            tris = trimestral[tri]
            allleave = Leave.objects.filter(start_date__year=tyear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(tyear)} </span>,   <span class="text-danger"> {tris[1]} </span>'
            get_tri = int(getTri)
            page = 'tri'

        # done: DONE
        elif getUnit != '0':
            allleave = Leave.objects.filter(employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,employee__curempdivision__unit_id=int(getUnit),  hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            unit_name = get_object_or_404(Unit, pk=int(getUnit))
            legend = f'Relatorio Licensa husi Divizaun  <span class="text-danger"> {unit_name.name} </span>'
            get_unit = int(getUnit)
            page = 'unit'
        # done: DONE
        elif getYear != '0':
            allleave = Leave.objects.filter(start_date__year=int(getYear), hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=int(getYear), hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(getYear)} </span>'
            get_year = int(getYear)
            page = 'year'
        else:
            allleave = Leave.objects.filter(start_date__year=int(tyear), hr_confirm=True, is_done=True).count()
            for i in leave_type:
                cleave = Leave.objects.filter(leave_type=i,start_date__year=int(tyear), hr_confirm=True, is_done=True).count()
                data.append([i, cleave])
            legend = f'Relatorio Licensa iha Tinan <span class="text-danger"> {int(tyear)} </span>'
            get_year = int(tyear)
            page = 'year'

    else:      
        allleave = Leave.objects.filter(start_date__year=int(tyear), hr_confirm=True, is_done=True).count()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, hr_confirm=True, is_done=True).count()
            data.append([i, cleave])
        legend = f'Painel Relatorio Licensa iha Tinan <span class="text-danger"> {tyear} </span>'
    
    context = {
        'title': 'Painel Relatorio Licensa','legend': legend, 
        'years': years, 'months': months, 'data': data, 'allleave':allleave, 'year': tyear, 'units':units,
        'trimestral':trimestral, 'error': error, 'page': page, 'datamonth':datamonth,
        'get_year': get_year, 'get_month': get_month, 'get_tri': get_tri, 'get_unit': get_unit,
    }
    return render(request, 'leave_report/dash.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveReportLeaveTypeList(request, pk, year):
    lt = get_object_or_404(LeaveType, pk=pk)
    allleave = None
    objects = Leave.objects.filter(leave_type=lt,start_date__year=year, is_active=True, hr_confirm=True, is_done=True)


    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {year}', 
        'objects': objects, 'allleave':allleave, 'year': year
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveReportLeaveTypeListAll(request, year):
    objects = Leave.objects.filter(start_date__year=year, is_active=True, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {year}', 
        'objects': objects, 'year': year
    }
    return render(request, 'leave_report/list.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrLeaveReportLeaveMonthTypeList(request, date):
    objects = Leave.objects.filter(start_date=date,hr_confirm=True, is_done=True)
    date_object = dt.strptime(date, "%Y-%m-%d")
    monthname = f_monthname(int(date_object.month))
    context = {
        'objects': objects,  'date':date,
        'title': 'Lista Licensa','legend': f'Lista Licensa iha loron {date_object.day}-{monthname}-{date_object.year}', 
    }
    return render(request, 'leave_report/list_day.html', context)


# REPORT DETAIL
# work: YEAR
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYear(request,pk, year):
    lt = get_object_or_404(LeaveType, pk=pk)
    objects = Leave.objects.filter(leave_type=lt,start_date__year=year, is_active=True, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa {lt.name} iha Tinan {year}', 
        'objects': objects, 'year': year
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearAll(request, year):
    objects = Leave.objects.filter(start_date__year=year, is_active=True, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {year}', 
        'objects': objects, 'year': year
    }
    return render(request, 'leave_report/list.html', context)

# work: UNIT
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveUnit(request,pk, pk2):
    lt = get_object_or_404(LeaveType, pk=pk)
    unit = get_object_or_404(Unit, pk=pk2)
    objects = Leave.objects.filter(leave_type=lt,employee__curempdivision__unit=unit,  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa {lt.name} iha Divizaun {unit.name}', 
        'objects': objects, 
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['adhrReportLeaveUnitmin','hr'])
def hrReportLeaveUnitAll(request,pk):
    unit = get_object_or_404(Unit, pk=pk)
    objects = Leave.objects.filter(employee__curempdivision__unit=unit,  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Divizaun {unit.name}', 
        'objects': objects
    }
    return render(request, 'leave_report/list.html', context)

# work: TRIMESTRAL
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveTri(request,pk, pk2):
    lt = get_object_or_404(LeaveType, pk=pk)
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    tri = int(pk2)-1
    tris = trimestral[tri]
    tyear = dt.now().year
    objects = Leave.objects.filter(leave_type=lt,start_date__year=tyear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa {lt.name}, Tinan, {tyear}, {tris[1]}', 
        'objects': objects, 
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['adhrReportLeaveUnitmin','hr'])
def hrReportLeaveTriAll(request):
    tyear = dt.now().year
    data = []
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    for tris in trimestral:
        objects = Leave.objects.filter(start_date__year=tyear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True)
        for i in objects:
            if i:
                data.append(i)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Trimestral, Tinan {tyear}', 
        'objects': data
    }
    return render(request, 'leave_report/list.html', context)


# work: MONTH
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonth(request, pk, month):
    tyear = dt.now().year
    monthname = f_monthname(int(month))
    lt = get_object_or_404(LeaveType, pk=pk)
    objects = Leave.objects.filter(leave_type=lt,start_date__year=tyear,start_date__month=month, is_active=True, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Tinan {tyear} Fulan {monthname}', 
        'objects': objects,
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonthAll(request, month):
    tyear = dt.now().year
    monthname = f_monthname(int(month))
    objects = Leave.objects.filter(start_date__year=tyear,start_date__month=month, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {tyear}, Fulan {monthname}', 
        'objects': objects
    }
    return render(request, 'leave_report/list.html', context)


# work: YEAR UNIT
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearUnit(request, pk,pk2, year):
    lt = get_object_or_404(LeaveType, pk=pk)
    unit = get_object_or_404(Unit, pk=pk2)
    objects = Leave.objects.filter(start_date__year=int(year),leave_type=lt,employee__curempdivision__unit_id=int(pk2),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa  {lt.name}, Tinan {year}, Divizaun {unit.name}', 
        'objects': objects, 'year': year
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearUnitAll(request,pk, year):
    unit = get_object_or_404(Unit, pk=pk)
    objects = Leave.objects.filter(start_date__year=int(year),employee__curempdivision__unit_id=int(pk),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Tinan {year}, Divizaun {unit.name}', 
        'objects': objects, 'year': year
    }
    return render(request, 'leave_report/list.html', context)


# work: YEAR MONTH
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonth(request, pk,year, month):
    monthname = f_monthname(int(month))
    lt = get_object_or_404(LeaveType, pk=pk)
    objects = Leave.objects.filter(leave_type=lt,start_date__year=year,start_date__month=month, is_active=True, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Tinan {year} Fulan {monthname}', 
        'objects': objects,
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonthAll(request,year, month):
    monthname = f_monthname(int(month))
    objects = Leave.objects.filter(start_date__year=year,start_date__month=month, hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {year}, Fulan {monthname}', 
        'objects': objects
    }
    return render(request, 'leave_report/list.html', context)

# work: MONTH UNIT
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonthUnit(request, pk, month, unit):
    tyear = dt.now().year
    monthname = f_monthname(int(month))
    lt = get_object_or_404(LeaveType, pk=pk)
    unit_name = get_object_or_404(Unit, pk=unit)
    objects = Leave.objects.filter(start_date__year=tyear,start_date__month=int(month),leave_type=lt,employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Tinan {tyear}, Fulan {monthname}, Divizaun {unit_name.name}', 
        'objects': objects,
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveMonthUnitAll(request, month, unit):
    tyear = dt.now().year
    monthname = f_monthname(int(month))
    unit_name = get_object_or_404(Unit, pk=unit)
    objects = Leave.objects.filter(start_date__year=int(tyear),start_date__month=int(month),employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {tyear}, Fulan {monthname}, Divizaun {unit_name.name}', 
        'objects': objects
    }
    return render(request, 'leave_report/list.html', context)

# work: YEAR TRIMESTRAL
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearTri(request,pk, year, gtri):
    lt = get_object_or_404(LeaveType, pk=pk)
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    tri = int(gtri)-1
    tris = trimestral[tri]
    objects = Leave.objects.filter(leave_type=lt,start_date__year=year, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa {lt.name}, Tinan{year}, {tris[1]}', 
        'objects': objects, 
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['adhrReportLeaveUnitmin','hr'])
def hrReportLeaveYearTriAll(request, year):
    data = []
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    for tris in trimestral:
        objects = Leave.objects.filter(start_date__year=year, start_date__month__gte=tris[2],  start_date__month__lte=tris[3],  is_active=True, hr_confirm=True, is_done=True)
        for i in objects:
            if i:
                data.append(i)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Trimestral, Tinan {year}', 
        'objects': data
    }
    return render(request, 'leave_report/list.html', context)


# work: YEAR MONTH UNIT
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearMonthUnit(request, pk,year, month, unit):
    monthname = f_monthname(int(month))
    lt = get_object_or_404(LeaveType, pk=pk)
    unit_name = get_object_or_404(Unit, pk=unit)
    objects = Leave.objects.filter(start_date__year=int(year),start_date__month=int(month),leave_type=lt,employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Tinan {year},Fulan {monthname}, Divizaun {unit_name.name}', 
        'objects': objects,
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearMonthUnitAll(request,year, month, unit):
    monthname = f_monthname(int(month))
    unit_name = get_object_or_404(Unit, pk=unit)
    objects = Leave.objects.filter(start_date__year=int(year),start_date__month=int(month),employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa iha Tinan {year}, Fulan {monthname}, Divizaun {unit_name.name}', 
        'objects': objects
    }
    return render(request, 'leave_report/list.html', context)


# work: YEAR TRIMESTRAL UNIT
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrReportLeaveYearTriUnit(request,pk, year, gtri, unit):
    lt = get_object_or_404(LeaveType, pk=pk)
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    tri = int(gtri)-1
    tris = trimestral[tri]
    unit_name = get_object_or_404(Unit, pk=unit)
    objects = Leave.objects.filter(leave_type=lt,start_date__year=int(year), start_date__month__gte=tris[2],  start_date__month__lte=tris[3], employee__curempdivision__unit_id=int(unit), hr_confirm=True, is_done=True)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa {lt.name}, Tinan{year}, {tris[1]}, Divizaun {unit_name.name}', 
        'objects': objects, 
    }
    return render(request, 'leave_report/list.html', context)

@login_required
@allowed_users(allowed_roles=['adhrReportLeaveUnitmin','hr'])
def hrReportLeaveYearTriUnitAll(request, year, unit):
    data = []
    unit_name = get_object_or_404(Unit, pk=unit)
    trimestral = np.array([[1,'Trimestre I','01','04'],[2,'Trimestre II','04','07'],\
				[3,'Trimestre III','07','10'],[4,'Trimestre IV','10','13']])
    for tris in trimestral:
        objects = Leave.objects.filter(start_date__year=int(year), start_date__month__gte=tris[2],  start_date__month__lte=tris[3], employee__curempdivision__unit_id=int(unit), is_active=True, hr_confirm=True, is_done=True)
        for i in objects:
            if i:
                data.append(i)
    context = {
        'title': 'Lista Licensa','legend': f'Lista Licensa Trimestral, Tinan {year}, Divizaun {unit_name.name}', 
        'objects': data
    }
    return render(request, 'leave_report/list.html', context)

# work: MONTH
# @login_required
# @allowed_users(allowed_roles=['admin','hr'])
# def hrReportLeaveDayMonth(request, date):
#     monthname = f_monthname(int(date.month))
#     objects = Leave.objects.filter(start_date=date.date(), hr_confirm=True, is_done=True)
#     context = {
#         'title': 'Lista Licensa','legend': f'Lista Licensa Loron {date.day}-{monthname}-{date.year}', 
#         'objects': objects,
#     }
#     return render(request, 'leave_report/list.html', context)