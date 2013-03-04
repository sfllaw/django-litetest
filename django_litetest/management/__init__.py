from __future__ import absolute_import

from django.core.management import get_commands
from django.utils.importlib import import_module


def load_command(name):
    """
    Given a command name, returns the Command class.

    (ImportError, AttributeError) are allowed to propagate.
    """
    app_name = get_commands()[name]
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command
