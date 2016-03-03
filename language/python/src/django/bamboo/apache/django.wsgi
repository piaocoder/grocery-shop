import os, sys
sys.path.append('/home/bamboo/grocery-shop/language/python/django')
sys.path.append('/var/www/django/bamboo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bamboo.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
