
============================
Django IPG HRMS attendance
============================


Quick start
============


1. Add 'attendance' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'attendance'
    ]

2. Include the attendance to project URLS like this::

    path('attendance/', include('attendance.urls')),

3. Run ``python manage.py migrate`` to create attendance model

4. Another Apps Need for this Apps:
    4.1. custom
    4.2. employee
    4.3. user