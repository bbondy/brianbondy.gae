from akismet import Akismet
import uuid
from secrets import *

def report_as_spam(comment, request):
  akismet_api = Akismet(key=Secrets.AKISMET_API_KEY, blog_url="http://www.brianbondy.com/")
  if akismet_api.verify_key():
    akismet_data = {
      'comment_type': 'comment',
#      'referrer': request.META.get('HTTP_REFERRER', ''),
#      'user_ip': request.META.get('REMOTE_ADDR', ''),
#      'user_agent': request.META.get('HTTP_USER_AGENT', ''),
      'comment_author': comment.name or '',
      'comment_author_email': comment.email or '',
      'comment_author_url': comment.homepage or '',
      }
    akismet_api.submit_spam(comment.body.encode('utf8', 'ignore'), akismet_data,  build_data=True)
    return True
  else:
    raise "Invalid Akismet key"
  return False

def report_as_good(comment, request):
  akismet_api = Akismet(key=Secrets.AKISMET_API_KEY, blog_url="http://www.brianbondy.com/")
  if akismet_api.verify_key():
    akismet_data = {
      'comment_type': 'comment',
#       'referrer': request.META.get('HTTP_REFERRER', ''),
#       'user_ip': request.META.get('REMOTE_ADDR', ''),
#       'user_agent': request.META.get('HTTP_USER_AGENT', ''),
      'comment_author': comment.name or '',
      'comment_author_email': comment.email or '',
      'comment_author_url': comment.homepage or '',
      }
    akismet_api.submit_ham(comment.body.encode('utf8', 'ignore'), akismet_data,  build_data=True)
  else:
    raise "Invalid Akismet key"


def is_spam(comment, request):
  akismet_api = Akismet(key=Secrets.AKISMET_API_KEY, blog_url="http://www.brianbondy.com/")
  if akismet_api.verify_key():
    akismet_data = {
      'comment_type': 'comment',
#      'referrer': request.headers['REFERRER'],
#      'user_ip': request.META.get('REMOTE_ADDR', ''),
#      'user_agent': request.headers['USER_AGENT', ''],
      'comment_author': comment.name or '',
      'comment_author_email': comment.email or '',
      'comment_author_url': comment.homepage or '',
    }

  if akismet_api.comment_check(comment.body.encode('utf8', 'ignore'), akismet_data,  build_data=True):
    return True
  else:
    return False
