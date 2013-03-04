=====================
 ``django-litetest``
=====================

A lightweight Django ``manage.py litetest`` command for quick unittest
runs.

If you've been developing in Django for a while, you probably have
plenty of tests written. This is great, but they probably take a long
time to run. If you do any sort of Test-Driven Development, slow tests
means a frustrating edit-test loop.

**django-litetest** helps you run quick, lightweight tests by doing a
few things:

* Use in-memory SQLite databases instead of your usual test
  databases,
* Use in-memory caches instead of your usual caches,
* If you're using South, creates models directly.

With **django-litetest**, fixing a bug becomes as quick as this:

1. Add a new test to reproduce the bug,
2. Run ``manage.py litetest`` *testname*,
3. Edit the code to fix the bug,
4. Run ``manage.py litetest`` *testname* again,
5. Run ``manage.py test`` to ensure that all your tests pass.


Installation
============

You can get a copy of the source by using::

    $ git clone https://github.com/sfllaw/django-litetest.git

This app requires:

* Python 2.6 or higher,
* Django 1.3 or higher,
* `SpatiaLite`_ (optional for GIS).

As well, this app is available from PyPi::

    $ pip install django-litetest

.. _SpatiaLite: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/


Configuration
=============

In your Django ``settings`` file:

* Add ``'django_litetest'`` to ``INSTALLED_APPS`` (after ``'south'``
  if you are using it),

* Add ``'LITETEST': True`` to each of the ``DATABASES`` you want sped up,

* Add ``'LITETEST': True`` to each of the ``CACHES`` you want sped up,

* If you are using South, set ``SOUTH_TESTS_MIGRATE = 'LITETEST'`` to
  avoid migrations.


Example ``settings`` file
-------------------------

::

    INSTALLED_APPS = (
        'south',
        'django_litetest',
        ...
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db',
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': 'db.example.com',
            'PORT': '',
            'LITETEST': True,
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': 'memcache.example.com:11211',
            'LITETEST': True,
        },
    }

    SOUTH_TESTS_MIGRATE = 'LITETEST'



Reporting bugs and submitting patches
=====================================

Please check our `issue tracker`_ for known bugs and feature requests.

We accept pull requests for fixes and new features.


Authors
=======

Simon Law <sfllaw@sfllaw.ca>


.. _issue tracker: https://github.com/sfllaw/django-litetest/issues
