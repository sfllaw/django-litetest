from __future__ import absolute_import

import textwrap

from django.conf import settings

from .. import load_command


TestCommand = load_command('test')


class Command(TestCommand):
    help = textwrap.dedent("""\
    Runs a lightweight version of the test suite.

    Like the built-in 'test' command, runs for the specified applications, or
    the entire site of no apps are specified.

    Unlike the 'test' command, will use in-memory databases and caches to speed
    up test runs. This is not as reliable as the full test suite, which should
    still be run afterwards.""")

    def handle(self, *args, **kwargs):
        self._shim_caches(settings)
        self._shim_databases(settings)
        self._shim_south(settings)
        return super(Command, self).handle(*args, **kwargs)

    def _shim_caches(self, settings):
        """Shim in local memory caches."""
        from django.core import cache, signals

        backend = 'django.core.cache.backends.locmem.LocMemCache'

        for alias, options in settings.CACHES.iteritems():
            # Ignore CACHES that are not configured for LITETEST
            if not options.get('LITETEST', False):
                continue

            # Ignore CACHES that are already using local memory caches
            if options.get('BACKEND', None) == backend:
                continue

            options['BACKEND'] = backend

            # Reset 'default' cache
            if alias == cache.DEFAULT_CACHE_ALIAS:
                if hasattr(cache.cache, 'close'):
                    signals.request_finished.disconnect(cache.cache.close)
                cache.cache = cache.get_cache(cache.DEFAULT_CACHE_ALIAS)

    def _shim_databases(self, settings):
        """Shim in SQLite in-memory databases."""
        from django.db import connections

        engine = 'django.db.backends.sqlite3'
        spatial_engine = 'django.contrib.gis.db.backends.spatialite'

        for alias, options in settings.DATABASES.iteritems():
            # Ignore DATABASES that are not configured for LITETEST
            if not options.get('LITETEST', False):
                continue

            # Ignore in-memory DATABASES
            options_engine = options.get('ENGINE', None)
            if options_engine in (engine, spatial_engine) and \
               options.get('NAME', None) == ':memory:':
                continue

            if options_engine.startswith('django.contrib.gis.db.backends'):
                options['ENGINE'] = spatial_engine
            else:
                options['ENGINE'] = 'django.db.backends.sqlite3'
            options['NAME'] = ':memory:'

            # Reset database connection
            if isinstance(connections._connections, dict):
                # Django 1.3
                conn = connections._connections.get(alias, None)
            else:
                conn = getattr(connections._connections, alias, None)
            if conn is not None:
                conn.close()
                if isinstance(connections._connections, dict):
                    # Django 1.3
                    del connections._connections[alias]
                else:
                    delattr(connections._connections, alias)

    def _shim_south(self, settings):
        if getattr(settings, 'SOUTH_TESTS_MIGRATE', None) == 'LITETEST':
            settings.SOUTH_TESTS_MIGRATE = False
