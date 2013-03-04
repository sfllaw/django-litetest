#!/usr/bin/env python

from setuptools import setup

import django_litetest


setup(
    name='django-litetest',
    version=django_litetest.__version__,
    description='A lightweight Django "test" command for quick unittest runs.',
    long_description=open('README.rst').read(),
    license='Apache Software License, version 2.0',

    author='Simon Law',
    author_email='sfllaw@sfllaw.ca',
    url='https://github.com/sfllaw/django-litetest',

    packages=['django_litetest',
              'django_litetest.management',
              'django_litetest.management.commands'],
    include_package_data=True,
    install_requires=['Django>=1.3'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],

    zip_safe=True,
)
