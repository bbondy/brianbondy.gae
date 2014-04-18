from google.appengine.api import users

def gae_mini_profiler_should_profile_production():
  return False#users.is_current_user_admin()

def gae_mini_profiler_should_profile_development():
  return False#users.is_current_user_admin()
