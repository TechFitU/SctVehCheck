#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # CHANGED manage.py will use development settings by
    # default. Change the DJANGO_SETTINGS_MODULE environment variable
    # for using the environment specific settings file.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sctvehcheck.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    # Wrap werkzeug debugger if DEBUG is on
    from django.conf import settings

    if settings.DEBUG:
        try:
            import django.views.debug
            import six
            from werkzeug.debug import DebuggedApplication


            def null_technical_500_response(request, exc_type, exc_value, tb):
                six.reraise(exc_type, exc_value, tb)


            django.views.debug.technical_500_response = null_technical_500_response
            application = DebuggedApplication(application, evalex=True,
                                              # Turning off pin security as DEBUG is True
                                              pin_security=False)
        except ImportError:
            pass
