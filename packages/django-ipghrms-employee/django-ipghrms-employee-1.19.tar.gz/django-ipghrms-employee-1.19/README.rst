
============================
Django IPG HRMS employee
============================


Quick start
============


1. Add 'employee' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'employee'
    ]

2. Include the employee to project URLS like this::

    path('employee/', include('employee.urls')),

3. Run ``python manage.py migrate`` to create employee model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user