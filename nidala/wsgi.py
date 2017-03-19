"""
WSGI config for nidala project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

# add the hellodjango project path into the sys.path
sys.path.append('/home/nidala/public_html/nidala')

# add the hellodjango project path into the sys.path
sys.path.append('/home/nidala/public_html')


# add the virtualenv site-packages path to the sys.path
sys.path.append('/usr/lib/python3.4/site-packages')

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nidala.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
