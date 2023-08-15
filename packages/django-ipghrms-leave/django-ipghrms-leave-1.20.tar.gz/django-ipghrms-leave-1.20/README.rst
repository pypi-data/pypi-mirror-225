
============================
Django IPG HRMS leave
============================


Quick start
============


1. Add 'leave' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'leave'
    ]

2. Include the leave to project URLS like this::

    path('leave/', include('leave.urls')),

3. Run ``python manage.py migrate`` to create leave model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user