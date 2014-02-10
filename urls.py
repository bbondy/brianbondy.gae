import logging
import settings
import json
import datetime
import time
import os

from app import *

from google.appengine.api import memcache

from google.appengine.ext.webapp import template
import layer_cache
import ho.pisa as pisa
from cStringIO import StringIO
from blog.models import * 
from spamController import *
from emailController import *

from flask import Flask, render_template, request, make_response, jsonify, Response, send_file, redirect, url_for
from dateutil import parser


from google.appengine.ext.db import Key
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None


@application.route(r'/newsItems/<int:id>', methods=['GET'])
def get_news_item(id):
  key = Key.from_path('NewsItem', str(id))
  news_item = NewsItem.get(key)
  return Response(json.dumps(news_item.jsonData, default=dthandler),  mimetype='application/json')

# JSON API
@application.route(r'/newsItems/all/', methods=['GET'], defaults={'drafts': None })
@application.route(r'/newsItems/', methods=['GET'], defaults={'drafts': False})
@application.route(r'/newsItems/tagged/<tag>/', methods=['GET'], defaults={'drafts': False})
@application.route(r'/newsItems/drafts/', methods=['GET'], defaults={'drafts': True})
@application.route(r'/newsItems/drafts/page/<int:page>', methods=['GET'], defaults={'drafts': True})
@application.route(r'/newsItems/page/<int:page>', methods=['GET'], defaults={'drafts': False})
@application.route(r'/newsItems/tagged/<tag>/page/<int:page>', methods=['GET'], defaults={'drafts': False})
@application.route(r'/newsItems/modified/recent/', methods=['GET'], defaults={'drafts': False, 'recently_modified': True})
@application.route(r'/newsItems/modified/recent/page/<int:page>', methods=['GET'], defaults={'drafts': False, 'recently_modified': True})
@application.route(r'/newsItems/posted/<int:year>')
@application.route(r'/newsItems/posted/<int:year>/page/<int:page>')
def get_news_items(id=None, drafts=False, page=1, count=5, order_by=None, tag='', recently_modified=False, year=None):
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

@application.route(r'/newsItems/<int:news_item_id>', methods=['DELETE'])
def delete_news_items(news_item_id):
  key = Key.from_path('NewsItem', str(news_item_id))
  news_item = NewsItem.get(key)
  news_item.delete()
  return Response(json.dumps({}),  mimetype='application/json')

@application.route(r'/newsItems/<int:news_item_id>', methods=['PUT'])
@application.route(r'/newsItems/', methods=['POST'])
def post_news_item(news_item_id=None):
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

  
@application.route(r'/blog/')
def blog_redirect():
  return redirect(url_for('index'))

@application.route(r'/')
@application.route(r'/blog/id/<int:news_item_id>/')    
@application.route(r'/blog/id/<int:news_item_id>/<title>/')    
@application.route(r'/page/<int:page>/')
@application.route(r'/drafts/', defaults={ 'drafts': True })
@application.route(r'/drafts/page/<int:page>/', defaults={ 'drafts': True })
@application.route(r'/blog/tagged/<tag>/')
@application.route(r'/blog/tagged/<tag>/page/<int:page>/')
@application.route(r'/blog/posted/recent/')
@application.route(r'/blog/posted/recent/page/<int:page>/')
@application.route(r'/blog/modified/recent/', defaults={'recently_modified' : True})
@application.route(r'/blog/modified/recent/page/<int:page>/', defaults={'recently_modified' : True})
@application.route(r'/blog/posted/<int:year>/')
@application.route(r'/blog/posted/<int:year>/page/<int:page>/')
@application.route(r'/blog/modified/<int:year>/', defaults={'recently_modified' : True})
@application.route(r'/blog/modified/<int:year>/page/<page>/', defaults={'recently_modified' : True})
def index(news_item_id=0, title=None, page=1, drafts=False, tag='', recently_modified=False, year=0):
  if page < 1:
    page = 1
  archive_list = NewsItem.get_year_list()
  tag_list = NewsItem.get_tag_list()
  return render_template('index.html', news_item_id=news_item_id, page=page, drafts=drafts, tag=tag, recently_modified=recently_modified, year=year, archive_list=archive_list, tag_list=tag_list);
  

#Blog comments
@application.route(r'/newsItems/<int:news_item_id>/comments')
def get_comments(news_item_id):
  news_item = NewsItem.get_by_id(news_item_id)
  comments = news_item.sorted_comments()
  logging.info(len(comments))
  logging.info(news_item._linkback);
  p = [x.jsonData for x in comments]
  return Response(json.dumps(p, default=dthandler),  mimetype='application/json')


@application.route(r'/comments/<int:comment_id>', methods=['PUT'])
@application.route(r'/newsItems/<int:news_item_id>/comments', methods=['POST'])
def post_comment(news_item_id=None, comment_id=None):
  if comment_id:
    comment = NewsItemComment.get_by_id(comment_id)
    if ('is_public' in request.json):
      comment.is_public = request.json['is_public'];
    else:
      comment.is_public = False

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
    comment.is_plublic = False
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

  send_email('bbondy@gmail.com', 'New comment posted by %s' % comment.name, comment.body)

  return Response(json.dumps(comment.jsonData, default=dthandler),  mimetype='application/json')


@application.route(r'/comments/', methods=['GET'])
def get_all_comments():
  news_item_comments = NewsItemComment.all()
  p = [x.allJSONData for x in news_item_comments]
  return Response(json.dumps(p),  mimetype='application/json')

@application.route(r'/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
  comment = NewsItemComment.get_by_id(int(comment_id))
  comment.delete();
  return Response(json.dumps({}),  mimetype='application/json')

@application.route(r'/other/whatsMyIP/')
def whats_my_ip():
  return render_template('whats_my_ip.html', client_IP=request.remote_addr)

@application.route(r'/resume/pdf/')
def resume_pdf():
  result = StringIO()
  html = render_template('resume_pdf.html')
  pdf = pisa.CreatePDF(html.encode('utf8'), result)
  val = result.getvalue();
  response = Response(result.getvalue())
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'attachment; filename=BrianRBondy_Resume.pdf'
  return response;

#RSS all, or by tag
@application.route(r'/feeds/rss/')
@application.route(r'/feeds/rss/<tagged>/')
def get_rss(tagged=''):
  rss_xml = NewsItem.get_rss_feed(tagged)
  return Response(rss_xml,  mimetype='application/rss+xml')


# Administer the site 
@application.route(r'/admin1/')
def admin_page():
  return render_template('admin/index.html', memcache_stats=memcache.get_stats())

@application.route(r'/admin1/newsItems/')
def admin_news_items():
  return render_template('admin/newsItems.html', news_item_list=NewsItem.all().order('-posted_date'));

@application.route(r'/admin1/newsItems/add/')
@application.route(r'/admin1/newsItems/<news_item_id>/')
def admin_news_item(news_item_id = 0):
  return render_template('admin/newsItem.html', news_item_id = news_item_id)


@application.route(r'/admin1/news_item_comments/')
def admin_news_item_comments():
  return render_template('admin/newsItemComments.html')

@application.route(r'/admin1/clear_memcache/')
def clear_memcache():
  memcache.flush_all()
  return redirect(url_for('admin_page'))

@application.route(r'/test/', defaults={'tmpl': 'test.html'} )
@application.route(r'/contact/', defaults={'tmpl': 'contact.html'})
@application.route('/about/', defaults={'tmpl': 'about.html'})
@application.route('/about/', defaults={'tmpl': 'about.html'})
@application.route(r'/other/', defaults={'tmpl': 'other.html'})
@application.route(r'/other/books/', defaults={'tmpl': 'books.html'})
@application.route(r'/other/advice/', defaults={'tmpl': 'advice.html'})
@application.route(r'/other/universityClasses/', defaults={'tmpl': 'university_classes.html'})
@application.route(r'/other/braille/', defaults={'tmpl': 'braille.html'})
@application.route(r'/other/morseCode/', defaults={'tmpl': 'morse_code.html'})
@application.route(r'/other/base64Encoding//', defaults={'tmpl':  'base64_encoding.html'})
@application.route(r'/other/binaryASCII/', defaults={'tmpl': 'binary_ASCII.html'})
@application.route(r'/other/URLEncoding/', defaults={'tmpl': 'URL_encoding.html'})
@application.route(r'/other/articles/', defaults={'tmpl': 'articles.html'})
@application.route(r'/other/faq/', defaults={'tmpl': 'faq.html'})
@application.route(r'/other/links/', defaults={'tmpl': 'links.html'})
@application.route(r'/talks/', defaults={'tmpl': 'talks.html'})
@application.route(r'/talks/2012-work-week-win8/', defaults={'tmpl': '2012-firefox-work-week/index.html'})
#aliases for when some of the other links were top level
@application.route(r'/articles/', defaults={'tmpl': 'articles.html'})
@application.route(r'/faq/', defaults={'tmpl': 'faq.html'})
@application.route(r'/links/', defaults={'tmpl': 'links.html'})
@application.route(r'/resume/', defaults={'tmpl': 'resume.html'})
@application.route(r'/test/', defaults={'tmpl': 'test.html'})
@application.route(r'/projects/', defaults={'tmpl': 'projects.html'})
@application.route(r'/mozilla/', defaults={'tmpl': 'mozilla.html'})
@application.route(r'/mozilla/cheatsheet/', defaults={'tmpl': 'mozilla_cheatsheet.html'})
@application.route(r'/mozilla/new/', defaults={'tmpl': 'mozilla_new.html'})
@application.route(r'/mozilla/xpcom/', defaults={'tmpl': 'mozilla_xpcom.html'})
@application.route(r'/mozilla/xulrunner/', defaults={'tmpl': 'mozilla_xulrunner.html'})
@application.route(r'/mozilla/extension/', defaults={'tmpl': 'mozilla_extension.html'})
@application.route(r'/stackexchange/', defaults={'tmpl': 'stackexchange.html'})
@application.route(r'/khanacademy/', defaults={'tmpl': 'khanacademy.html'})
@application.route(r'/khanacademy/cheatsheet/', defaults={'tmpl': 'khanacademy_cheatsheet.html'})
@application.route(r'/math/', defaults={'tmpl': 'math.html'})
@application.route(r'/math/pi/', defaults={'tmpl': 'pi.html'})
@application.route(r'/math/primes/', defaults={'tmpl': 'primes.html'})
@application.route(r'/math/numberTheory/', defaults={'tmpl': 'number_theory.html'})
@application.route(r'/math/graphTheory/', defaults={'tmpl': 'graph_theory.html'})
@application.route(r'/compression/', defaults={'tmpl': 'compression.html'})
@application.route(r'/compression/huffman/', defaults={'tmpl': 'huffman.html' })
@application.route(r'/compression/BWT/', defaults={'tmpl': 'BWT.html'})
@application.route(r'/compression/PPM/', defaults={'tmpl': 'PPM.html'})
@application.route(r'/math/mathTricks/', defaults={'tmpl': 'math_tricks.html'})

#Web apps
@application.route(r'/webapp_install/', defaults={'tmpl': 'webapp_install.html'})

#Twitter list links
@application.route(r'/stackexchange-twitter/cooking/', defaults={'tmpl': 'StackExchangeTwitter/Cooking.html'})
@application.route(r'/stackexchange-twitter/gamedevelopment/', defaults={'tmpl': 'StackExchangeTwitter/GameDevelopment.html'})
@application.route(r'/stackexchange-twitter/gaming/', defaults={'tmpl': 'StackExchangeTwitter/Gaming.html'})
@application.route(r'/stackexchange-twitter/mathematics/', defaults={'tmpl': 'StackExchangeTwitter/Mathematics.html'})
@application.route(r'/stackexchange-twitter/photography/', defaults={'tmpl': 'StackExchangeTwitter/Photography.html'})
@application.route(r'/stackexchange-twitter/serverfault/', defaults={'tmpl': 'StackExchangeTwitter/ServerFault.html'})
@application.route(r'/stackexchange-twitter/stackapps/', defaults={'tmpl': 'StackExchangeTwitter/StackApps.html'})
@application.route(r'/stackexchange-twitter/stackoverflow/', defaults={'tmpl': 'StackExchangeTwitter/StackOverflow.html'})
@application.route(r'/stackexchange-twitter/statisticalanalysis/', defaults={'tmpl': 'StackExchangeTwitter/StatisticalAnalysis.html'})
@application.route(r'/stackexchange-twitter/superuser/', defaults={'tmpl': 'StackExchangeTwitter/SuperUser.html'})
@application.route(r'/stackexchange-twitter/ubuntu/', defaults={'tmpl': 'StackExchangeTwitter/AskUbuntu.html'})
@application.route(r'/stackexchange-twitter/webapplications/', defaults={'tmpl': 'StackExchangeTwitter/WebApplications.html'})
@application.route(r'/stackexchange-twitter/webmasters/', defaults={'tmpl': 'StackExchangeTwitter/WebMasters.html'})
@application.route(r'/stackexchange-twitter/englishusage/', defaults={'tmpl': 'StackExchangeTwitter/EnglishLanguageandUsage.html'})
@application.route(r'/stackexchange-twitter/programmers/', defaults={'tmpl': 'StackExchangeTwitter/Programmers.html'})
@application.route(r'/stackexchange-twitter/texlatex/', defaults={'tmpl': 'StackExchangeTwitter/TeX-LaTeX.html'})
@application.route(r'/stackexchange-twitter/theoreticalcs/', defaults={'tmpl': 'StackExchangeTwitter/TheoreticalComputerScience.html'})
@application.route(r'/stackexchange-twitter/android/', defaults={'tmpl': 'StackExchangeTwitter/Android.html'})
@application.route(r'/stackexchange-twitter/apple/', defaults={'tmpl': 'StackExchangeTwitter/Apple.html'})
@application.route(r'/stackexchange-twitter/doityourself/', defaults={'tmpl': 'StackExchangeTwitter/DoItYourself.html'})
@application.route(r'/stackexchange-twitter/electronics/', defaults={'tmpl': 'StackExchangeTwitter/Electronics.html'})
@application.route(r'/stackexchange-twitter/gis/', defaults={'tmpl': 'StackExchangeTwitter/GeographicInformationSystems.html'})
@application.route(r'/stackexchange-twitter/unix/', defaults={'tmpl': 'StackExchangeTwitter/Unix.html'})
@application.route(r'/stackexchange-twitter/wordpress/', defaults={'tmpl': 'StackExchangeTwitter/Wordpress.html'})

#LinkedIn list links
@application.route(r'/stackexchange-linkedin/cooking/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Cooking.html'})
@application.route(r'/stackexchange-linkedin/gamedevelopment/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-GameDevelopment.html'})
@application.route(r'/stackexchange-linkedin/gaming/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Gaming.html'})
@application.route(r'/stackexchange-linkedin/mathematics/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Mathematics.html'})
@application.route(r'/stackexchange-linkedin/photography/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Photography.html'})
@application.route(r'/stackexchange-linkedin/serverfault/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-ServerFault.html'})
@application.route(r'/stackexchange-linkedin/stackapps/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-StackApps.html'})
@application.route(r'/stackexchange-linkedin/stackoverflow/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-StackOverflow.html'})
@application.route(r'/stackexchange-linkedin/statisticalanalysis/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-StatisticalAnalysis.html'})
@application.route(r'/stackexchange-linkedin/superuser/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-SuperUser.html'})
@application.route(r'/stackexchange-linkedin/ubuntu/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-AskUbuntu.html'})
@application.route(r'/stackexchange-linkedin/webapplications/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-WebApplications.html'})
@application.route(r'/stackexchange-linkedin/webmasters/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-WebMasters.html'})
@application.route(r'/stackexchange-linkedin/englishusage/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-EnglishLanguageandUsage.html'})
@application.route(r'/stackexchange-linkedin/programmers/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Programmers.html'})
@application.route(r'/stackexchange-linkedin/texlatex/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-TeX-LaTeX.html'})
@application.route(r'/stackexchange-linkedin/theoreticalcs/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-TheoreticalComputerScience.html'})
@application.route(r'/stackexchange-linkedin/android/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Android.html'})
@application.route(r'/stackexchange-linkedin/apple/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Apple.html'})
@application.route(r'/stackexchange-linkedin/doityourself/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-DoItYourself.html'})
@application.route(r'/stackexchange-linkedin/electronics/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Electronics.html'})
@application.route(r'/stackexchange-linkedin/gis/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-GeographicInformationSystems.html'})
@application.route(r'/stackexchange-linkedin/unix/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Unix.html'})
@application.route(r'/stackexchange-linkedin/wordpress/', defaults={'tmpl': 'StackExchangeTwitter/LinkedIn-Wordpress.html'})

#Facebook list links
@application.route(r'/stackexchange-facebook/cooking/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Cooking.html'})
@application.route(r'/stackexchange-facebook/gamedevelopment/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-GameDevelopment.html'})
@application.route(r'/stackexchange-facebook/gaming/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Gaming.html'})
@application.route(r'/stackexchange-facebook/mathematics/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Mathematics.html'})
@application.route(r'/stackexchange-facebook/photography/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Photography.html'})
@application.route(r'/stackexchange-facebook/serverfault/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-ServerFault.html'})
@application.route(r'/stackexchange-facebook/stackapps/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-StackApps.html'})
@application.route(r'/stackexchange-facebook/stackoverflow/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-StackOverflow.html'})
@application.route(r'/stackexchange-facebook/statisticalanalysis/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-StatisticalAnalysis.html'})
@application.route(r'/stackexchange-facebook/superuser/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-SuperUser.html'})
@application.route(r'/stackexchange-facebook/ubuntu/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-AskUbuntu.html'})
@application.route(r'/stackexchange-facebook/webapplications/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-WebApplications.html'})
@application.route(r'/stackexchange-facebook/webmasters/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-WebMasters.html'})
@application.route(r'/stackexchange-facebook/englishusage/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-EnglishLanguageandUsage.html'})
@application.route(r'/stackexchange-facebook/programmers/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Programmers.html'})
@application.route(r'/stackexchange-facebook/texlatex/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-TeX-LaTeX.html'})
@application.route(r'/stackexchange-facebook/theoreticalcs/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-TheoreticalComputerScience.html'})
@application.route(r'/stackexchange-facebook/android/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Android.html'})
@application.route(r'/stackexchange-facebook/apple/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Apple.html'})
@application.route(r'/stackexchange-facebook/doityourself/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-DoItYourself.html'})
@application.route(r'/stackexchange-facebook/electronics/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Electronics.html'})
@application.route(r'/stackexchange-facebook/gis/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-GeographicInformationSystems.html'})
@application.route(r'/stackexchange-facebook/unix/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Unix.html'})
@application.route(r'/stackexchange-facebook/wordpress/', defaults={'tmpl': 'StackExchangeTwitter/Facebook-Wordpress.html'})

# Expected age list links
@application.route(r'/stackexchange/expected-age/cooking/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Cooking.html'})
@application.route(r'/stackexchange/expected-age/gamedevelopment/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-GameDevelopment.html'})
@application.route(r'/stackexchange/expected-age/gaming/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Gaming.html'})
@application.route(r'/stackexchange/expected-age/mathematics/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Mathematics.html'})
@application.route(r'/stackexchange/expected-age/photography/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Photography.html'})
@application.route(r'/stackexchange/expected-age/serverfault/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-ServerFault.html'})
@application.route(r'/stackexchange/expected-age/stackapps/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-StackApps.html'})
@application.route(r'/stackexchange/expected-age/stackoverflow/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-StackOverflow.html'})
@application.route(r'/stackexchange/expected-age/statisticalanalysis/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-StatisticalAnalysis.html'})
@application.route(r'/stackexchange/expected-age/superuser/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-SuperUser.html'})
@application.route(r'/stackexchange/expected-age/ubuntu/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-AskUbuntu.html'})
@application.route(r'/stackexchange/expected-age/webapplications/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-WebApplications.html'})
@application.route(r'/stackexchange/expected-age/webmasters/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Webmasters.html'})
@application.route(r'/stackexchange/expected-age/englishusage/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-EnglishLanguageandUsage.html'})
@application.route(r'/stackexchange/expected-age/programmers/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Programmers.html'})
@application.route(r'/stackexchange/expected-age/texlatex/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-TeX-LaTeX.html'})
@application.route(r'/stackexchange/expected-age/theoreticalcs/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-TheoreticalComputerScience.html'})
@application.route(r'/stackexchange/expected-age/android/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Android.html'})
@application.route(r'/stackexchange/expected-age/apple/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Apple.html'})
@application.route(r'/stackexchange/expected-age/doityourself/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-DoItYourself.html'})
@application.route(r'/stackexchange/expected-age/electronics/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Electronics.html'})
@application.route(r'/stackexchange/expected-age/gis/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-GeographicInformationSystems.html'})
@application.route(r'/stackexchange/expected-age/unix/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Unix.html'})
@application.route(r'/stackexchange/expected-age/wordpress/', defaults={'tmpl': 'StackExchangeTwitter/ExpectedAge-Wordpress.html'})
@application.route(r'/facebook/pimemorize/', defaults={'tmpl': 'facebook/pimemorize.html'})
@application.route(r'/maze/', defaults={'tmpl': 'maze.html'})  
def direct_template(tmpl, name=None):
  return render_template(tmpl, name=name);
