import os
import sys

sys.path.append('/home/sunny/')
sys.path.append('/home/sunny/tweetanalyzer')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetanalyzer.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
