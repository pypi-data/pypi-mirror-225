
============================
Django IPG HRMS main
============================


Quick start
============


1. Add 'main' to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = [
        'main'
    ]

2. Include the main to project URLS like this::

    path('main/', include('main.urls')),

3. Run ``python manage.py migrate`` to create main model

4. Another Apps Need for this Apps::
    4.1. custom::
    4.2. employee::
    4.3. user