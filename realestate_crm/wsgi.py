"""
WSGI config for realestate_crm project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_crm.settings')

application = get_wsgi_application()
