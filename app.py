import os
from flask import Flask
import gae_mini_profiler.profiler
import gae_mini_profiler.templatetags

application = Flask(__name__)
err = application.errorhandler
route = application.route

options = application.create_jinja_environment()

application.jinja_env.globals['profiler_includes'] = gae_mini_profiler.templatetags.profiler_includes
application = gae_mini_profiler.profiler.ProfilerWSGIMiddleware(application)
application.errorhandler = err
application.route = route

# A singleton shared across requests
class App(object):
  # This gets reset every time a new version is deployed on
  # a live server.  It has the form major.minor where major
  # is the version specified in app.yaml and minor auto-generated
  # during the deployment process.  Minor is always 1 on a dev
  # server.
  version = os.environ['CURRENT_VERSION_ID']
