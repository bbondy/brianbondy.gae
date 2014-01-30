# Standard Python imports.
#import os
#import sys
#import logging

#import sys
#sys.path.insert(0, 'depends')
#sys.path.insert(0, 'reportlab.zip')

import webapp2;
import urls;

# Create a Django application for WSGI.
application = webapp2.WSGIApplication(urls.routes, debug=True);
