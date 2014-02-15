from google.appengine.api import memcache
from blog.models import * 
from flask import render_template, redirect, url_for
from google.appengine.api import users

def admin_page():
  logging.info('logged in with: ' + str(users.get_current_user()));
  return render_template('admin/index.html', memcache_stats=memcache.get_stats())

def admin_news_items():
  return render_template('admin/newsItems.html', news_item_list=NewsItem.all().order('-posted_date'));

def admin_news_item(news_item_id = 0):
  return render_template('admin/newsItem.html', news_item_id = news_item_id)

def admin_news_item_comments():
  return render_template('admin/newsItemComments.html')

def clear_memcache():
  memcache.flush_all()
  return redirect(url_for('admin_page'))
