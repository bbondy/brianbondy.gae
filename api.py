import logging
import json
import datetime

import layer_cache
from blog.models import * 
from spamController import *
from emailController import *

from app import *
from flask import request, Response
from dateutil import parser

from google.appengine.api import memcache

# TODO: Should abstract away this usage
from google.appengine.ext.db import Key
from google.appengine.api import users

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None

@application.errorhandler(401)
def custom_401(error):
    return Response('You must be logged in', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})

def get_news_items(drafts=False, page=1, order_by=None, tag='', recently_modified=False, year=None):
  if 'uncached' in request.args or drafts:
    return get_news_items_uncached(drafts, page, order_by, tag, recently_modified, year)
  return get_news_items_cached(drafts, page, order_by, tag, recently_modified, year)
  
@layer_cache.cache_with_key_fxn(lambda drafts, page, order_by, tag, recently_modified, year: "get_news_items_%s_%s_%s_%s_%s_%s" % (drafts, page, order_by, tag, recently_modified, year))
def get_news_items_cached(drafts=False, page=1, order_by=None, tag='', recently_modified=False, year=None):
  return get_news_items_uncached(drafts, page, order_by, tag, recently_modified, year)

def get_news_items_uncached(drafts=False, page=1, order_by=None, tag='', recently_modified=False, year=None):
  if 'count' in request.args:
    count = int(request.args['count'])
  else:
    count = 2
  if page < 1:
    page = 1
  order_by = '-posted_date'
  if recently_modified:
    order_by = '-last_modified_date'

  page_index = page - 1
  if drafts == None:
    news_items = NewsItem.all().order(order_by)
  elif drafts:
    news_items = NewsItem.get_all_drafts(page_index, count, order_by=order_by)
  elif tag:
    news_items = NewsItem.get_all_by_tag(tag, page_index, count, order_by)
  elif year:
    news_items = NewsItem.get_all_by_year(year, page_index, count, order_by)
  else:
    news_items = NewsItem.get_all(page_index, count, order_by=order_by)
  p = [x.jsonData for x in news_items]
  return Response(json.dumps(p, default=dthandler),  mimetype='application/json')

def get_news_item(id):
  if 'uncached' not in request.args:
    logging.info('getting cached news item')
    return get_news_item_cached(id)

  logging.info('getting uncached news item')
  key = Key.from_path('NewsItem', str(id))
  news_item = NewsItem.get(key)
  return Response(json.dumps(news_item.jsonData, default=dthandler),  mimetype='application/json')

@layer_cache.cache_with_key_fxn(lambda id: "get_news_item_%s" % (id))
def get_news_item_cached(id):
  news_item = NewsItem.get_by_id(id)
  return Response(json.dumps(news_item.jsonData, default=dthandler),  mimetype='application/json')

@layer_cache.cache_with_key_fxn(lambda news_item_id: "get_comments_%s" % (news_item_id))
def get_comments(news_item_id):
  key = Key.from_path('NewsItem', str(news_item_id))
  # Don't use get_by_id here since this can be a draft and that function
  # doesn't return draft items
  news_item = NewsItem.get(key)
  news_item.add_meta_fields()
  comments = news_item.sorted_comments()
  p = [x.jsonData for x in comments]
  return Response(json.dumps(p, default=dthandler),  mimetype='application/json')

# Note you can also call this from non admin, but with restricted allowance
# If the user is not authorized, is_public property will be ignored and will sipmly
# be set to false.
def post_comment(news_item_id=None, comment_id=None):
  if comment_id:
    comment = NewsItemComment.get_by_id(comment_id)
    comment.is_public = False
    if users.get_current_user():
      if ('is_public' in request.json):
        comment.is_public = request.json['is_public'];

    # Should we report as good?
    if ('report_as_good' in request.json):
      if report_as_good(comment, request):
        logging.info('reported as good!')
      else:
        logging.info('FAILED TO reported as good!')

    # Should we report as spam?
    if ('report_as_spam' in request.json):
      if report_as_spam(comment, request):
        logging.info('reported as spam!')
      else:
        logging.info('FAILED TO reported as spam!')

  else:
    comment = NewsItemComment.create()
    comment.is_public = False
    if news_item_id:
      news_item = NewsItem.get_by_id(news_item_id)
      comment.news_item = news_item

  # TODO: Most of this code can go in the model with a fromJSONData function
  comment.name = request.json['name']
  comment.email = request.json['email']
  comment.body = request.json['body']
  comment.homepage = request.json['homepage']
  comment.posted_date = datetime.datetime.now()
  comment.poster_ip = request.remote_addr

  comment.put()

  # If this was a new comment, then send an email about it
  if not comment_id: 
    send_email('bbondy@gmail.com', 'New comment posted by %s' % comment.name, comment.body)

  if comment.is_public:
    memcache.flush_all()

  return Response(json.dumps(comment.jsonData, default=dthandler),  mimetype='application/json')

# Does nothing if the user is not authenticated
def delete_news_item(news_item_id):
  if not users.get_current_user():
    abort(401)

  logging.info('Getting news item id: ' + str(news_item_id))
  news_item = NewsItem.get_by_id(news_item_id)
  news_item.delete()
  return Response(json.dumps({}),  mimetype='application/json')

def post_news_item(news_item_id=None):
  if not users.get_current_user():
    abort(401)

  if news_item_id:
    key = Key.from_path('NewsItem', str(news_item_id))
    news_item = NewsItem.get(key)
    news_item.clearTags();
  else:
    news_item = NewsItem.create()

  # TODO: Most of this code can go in the model with a fromJSONData function
  news_item.title = request.json['title']
  news_item.body = request.json['body']
  news_item.draft = request.json['draft']
  news_item.posted_date = parser.parse(request.json['posted_date'])
  news_item.last_modified_date = parser.parse(request.json['last_modified_date'])
  news_item.put();

  # Loop through the tags to add them
  for tag_name in request.json['tags']:
    tag_name = tag_name.strip()
    if tag_name == '':
      continue  

    tag = Tag(key_name=tag_name, tag=tag_name)
    tag.put()
    news_item_tag = NewsItemTag()
    news_item_tag.tag = tag.key()
    news_item_tag.news_item = news_item.key()
    news_item_tag.put()

  return Response(json.dumps(news_item.jsonData, default=dthandler),  mimetype='application/json')

# Returns an empty array if the user is not authorized to view all comments at once
def get_all_comments():
  if not users.get_current_user():
    abort(401)

  news_item_comments = NewsItemComment.all().order('-posted_date')
  p = [x.allJSONData for x in news_item_comments]
  return Response(json.dumps(p),  mimetype='application/json')

# Does nothing if the user is not authenticated
def delete_comment(comment_id):
  if not users.get_current_user():
    abort(401)

  comment = NewsItemComment.get_by_id(int(comment_id))
  comment.delete();
  return Response(json.dumps({}),  mimetype='application/json')


