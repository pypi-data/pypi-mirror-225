
============================
Django IPG HRMS notification
============================


Quick start
============


1. Add 'notification' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'notification'
    ]

2. Include the notification to project URLS like this::

    path('notification/', include('notification.urls')),

3. Run ``python manage.py migrate`` to create notification model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user