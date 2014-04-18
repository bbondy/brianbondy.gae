import logging

def appstats_should_record(env):
  from gae_mini_profiler.config import should_profile
  if should_profile():
      return True

def gae_mini_profiler_should_profile_production():
  from google.appengine.api import users
  return users.is_current_user_admin()

def gae_mini_profiler_should_profile_development():
  from google.appengine.api import users
  return users.is_current_user_admin()
