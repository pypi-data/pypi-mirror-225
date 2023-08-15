import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from django.contrib import messages

@login_required
def LeaveChartDash(request):
    group = request.user.groups.all()[0].name
    context = {
        'group': group,
        'title': 'Grafiku Licensa', 'legend': 'Grafiku Licensa'
    }
    return render(request, 'leave_chart/chart_leave.html', context)