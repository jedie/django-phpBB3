# coding: utf-8

"""
    views
    ~~~~~

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from django.core import management
from django.http import HttpResponse


def migrate(request):
    """
    Only usefull for developing:
    Use the django traceback page if a error appears ;) 
    """
    management.call_command("reset", "djangobb_forum", interactive=False)
    management.call_command("phpbb2djangobb",
        cleanup_users=3
    )
    return HttpResponse("Migration without errors, OK!")
