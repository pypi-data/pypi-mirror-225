import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from employee.models import Employee, CurEmpDivision, FormalEducation, LocationTL, Country
from contract.models import EmpPosition
from custom.models import EducationLevel, Unit, Department, Municipality
from settings_app.user_utils import c_unit, c_dep
from leave.models import LeaveCount, Leave, LeavePeriod, LeaveType
from datetime import datetime as dt
from settings_app.utils import getnewid, f_monthname

def count_leave(emp):
    leave_type = LeaveType.objects.all()
    leave = []
    l_name = []
    name = []
    for l in leave_type:

        period = LeavePeriod.objects.filter(employee=emp, is_active=True).last()
        lcount = Leave.objects.filter(employee=emp, leave_period=period, leave_type=l, hr_confirm=True, is_done=True).count()
        leave.append(lcount)
        name.append(l.name)
        leave.append(lcount)
        l_name.append([l.name])
    return name, leave

class APIEmpLeave(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        object = list()
        group = request.user.groups.all()[0].name
        employee = Employee.objects.filter(status_id=1)
        categories = list()
        data = list()
        month = datetime.date.today().strftime("%B")
        year = datetime.date.today().strftime("%Y")
        legend = f'Summary all Staff as of  {month} {year}'


        al = list()
        sicleave = list()
        spleave = list()
        mtleave = list()
        ptleave = list()
        chilleave = list()

        for emp in employee:
            period = LeavePeriod.objects.filter(employee=emp, is_active=True).last()
            aleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=1, hr_confirm=True, is_done=True).count()
            sickleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=2, hr_confirm=True, is_done=True).count()
            specialleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=3, hr_confirm=True, is_done=True).count()
            matleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=4, hr_confirm=True, is_done=True).count()
            patleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=5, hr_confirm=True, is_done=True).count()
            childleave = Leave.objects.filter(employee=emp, leave_period=period, leave_type_id=6, hr_confirm=True, is_done=True).count()
            categories.append(f'{emp.first_name} {emp.last_name}')
            al.append(aleave)
            sicleave.append(sickleave)
            spleave.append(specialleave)
            mtleave.append(matleave)
            ptleave.append(patleave)
            chilleave.append(childleave)
        data = {
            
            'categories': categories, 'legend': legend,
            'al': al,'sicleave': sicleave,'spleave': spleave,
            'matleave': mtleave, 'patleave':ptleave, 'chileave': childleave
        }

        return Response(data)


class APIEmpLeaveType(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        label = list()
        obj = list()
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            annual_leave = Leave.objects.filter(leave_type=i,leave_period__is_active=True, is_active=True, hr_confirm=True, is_done=True).count()
            obj.append({
                'name': i.name,
                'y': annual_leave
            })
        data = { 'label': 'All staff total days Leaves', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveType2(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,year, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i, start_date__year=year,  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveType3(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,year,month, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i, start_date__year=year, start_date__month=month,  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': 'All staff total days Leaves by Year and Month', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveUnit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, unit, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        unit_name = get_object_or_404(Unit, pk=unit)
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,employee__curempdivision__unit_id=unit,  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa iha {unit_name.name}' , 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveMonth(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,month, format=None):
        label = []
        obj = []
        tyear = dt.now().year
        monthname = f_monthname(int(month))
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, start_date__month=int(month),  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {tyear} fulan {monthname}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveYearUnit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,unit, year, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        unit_name = get_object_or_404(Unit, pk=unit)
        for i in leave_type:
            cleave = Leave.objects.filter(start_date__year=int(year),leave_type=i,employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year} Divizaun {unit_name.name}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveYearMonth(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,month, year, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        monthname = f_monthname(int(month))
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=int(year), start_date__month=int(month),  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year} Fulan {monthname}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveMonthUnit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,month,unit, format=None):
        label = []
        obj = []
        tyear = dt.now().year
        monthname = f_monthname(int(month))
        unit_name = get_object_or_404(Unit, pk=unit)
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, start_date__month=int(month), employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {tyear}, Fulan {monthname}, Divizaun {unit_name.name} ', 
        'obj': obj,  'label2':label}
        return Response(data)
    

class APIEmpLeaveTri(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, tri, format=None):
        trimestral = np.array([[1,'Trimetre I','01','04'],[2,'Trimetre II','04','07'],\
				[3,'Trimetre III','07','10'],[4,'Trimetre IV','10','13']])
        gtri = int(tri)-1
        tris = trimestral[gtri]
        tyear = dt.now().year
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=tyear, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {tyear} {tris[1]}', 
        'obj': obj,  'label2':label}
        return Response(data)


class APIEmpLeaveYearTri(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, year,tri, format=None):
        trimestral = np.array([[1,'Trimetre I','01','04'],[2,'Trimetre II','04','07'],\
				[3,'Trimetre III','07','10'],[4,'Trimetre IV','10','13']])
        gtri = int(tri)-1
        tris = trimestral[gtri]
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=year, start_date__month__gte=tris[2],  start_date__month__lte=tris[3], hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year} {tris[1]}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveYearMonthUnit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,month, year, unit, format=None):
        label = []
        obj = []
        leave_type = LeaveType.objects.all()
        monthname = f_monthname(int(month))
        unit_name = get_object_or_404(Unit, pk=unit)
        for i in leave_type:
            cleave = Leave.objects.filter(start_date__year=int(year),start_date__month=int(month),leave_type=i,employee__curempdivision__unit_id=int(unit),  hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year}, Fulan {monthname}, Divizaun {unit_name.name}', 
        'obj': obj,  'label2':label}
        return Response(data)

class APIEmpLeaveYearTriUnit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, year,tri,unit, format=None):
        trimestral = np.array([[1,'Trimetre I','01','04'],[2,'Trimetre II','04','07'],\
				[3,'Trimetre III','07','10'],[4,'Trimetre IV','10','13']])
        gtri = int(tri)-1
        tris = trimestral[gtri]
        label = []
        obj = []
        unit_name = get_object_or_404(Unit, pk=unit)
        leave_type = LeaveType.objects.all()
        for i in leave_type:
            cleave = Leave.objects.filter(leave_type=i,start_date__year=year, start_date__month__gte=tris[2],  start_date__month__lte=tris[3],employee__curempdivision__unit_id=int(unit), hr_confirm=True, is_done=True).count()
            obj.append(cleave)
            label.append(i.name)
        data = { 'label': f'Distribuisaun Licensa Tinan {year}, {tris[1]}, {unit_name.name}', 
        'obj': obj,  'label2':label}
        return Response(data)