import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import employee
from settings_app.decorators import allowed_users
from django.contrib import messages
from employee.models import CurEmpDivision, Employee
from leave.models import Leave, LeaveCount, LeaveDelegate
from leave.forms import LeaveDelegateForm2, LeaveForm, LeaveDelegateForm1
from settings_app.utils import getnewid
from settings_app.user_utils import c_staff

###