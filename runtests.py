#!/usr/bin/env python
import sys
import gevent.monkey
gevent.monkey.patch_all()

try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass

import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'ATOMIC_REQUESTS': False,
            'CONN_MAX_AGE': 0,
        }
    },
    INSTALLED_APPS=(
        'tests',
        'django_db_geventpool',
    ),
    USE_TZ=True,
)
django.setup()

test_runner = DiscoverRunner(verbosity=2)

failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(failures)
