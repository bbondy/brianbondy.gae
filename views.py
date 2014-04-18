import logging
import layer_cache
import ho.pisa as pisa
from cStringIO import StringIO
from blog.models import * 
from flask import render_template, request, Response

#@layer_cache.cache_with_key_fxn(lambda news_item_id, page, drafts, tag, recently_modified, year: "index_%s_%s_%s_%s_%s_%s" % (news_item_id, page, drafts, tag, recently_modified, year))
def index(news_item_id=0, page=1, drafts=False, tag='', recently_modified=False, year=0):
  if page < 1:
    page = 1

  page_index = page - 1
  count_per_page = 2

  archive_list = NewsItem.get_year_list()
  tag_list = NewsItem.get_tag_list()
  order_by = '-posted_date'


  if drafts == None:
    news_items = NewsItem.all()
  elif drafts:
    news_items = NewsItem.get_all_drafts(page_index, count_per_page, order_by)
  elif tag:
    news_items = NewsItem.get_all_by_tag(tag, page_index, count_per_page, order_by)
  elif year:
    news_items = NewsItem.get_all_by_year(year, page_index, count_per_page, order_by)
  else:
    news_items = NewsItem.get_all(page_index, count_per_page, order_by=order_by)
  available = len(news_items)
  logging.info('available is: %i' % available);

  current_url = request.url.split('/page/')[0]
  if current_url[len(current_url) - 1] != '/':
    current_url += '/'
  if page != 1:
    prev_url = current_url + 'page/%i/' % (page-1)
    logging.info('prev url is: ' + prev_url)
  else:
    prev_url = ''

  if available >= count_per_page:
    logging.info('available: %i, count: %i' % (available, page * count_per_page))
    next_url = current_url + 'page/%i/' % (page+1)
    logging.info('next url is: ' + next_url)
  else:
    next_url = ''
  
  return render_template('index.html', news_item_id=news_item_id, page=page, drafts=drafts, tag=tag, recently_modified=recently_modified, year=year, archive_list=archive_list, tag_list=tag_list, count=count_per_page, available=available, prev_url=prev_url, next_url=next_url);

#@layer_cache.cache_with_key_fxn(lambda tagged: "tagged_%s" % (tagged))
def get_rss(tagged=''):
  rss_xml = NewsItem.get_rss_feed(tagged)
  return Response(rss_xml,  mimetype='application/rss+xml')

#@layer_cache.cache_with_key_fxn(lambda tmpl: "direct_template_%s" % (tmpl))
def direct_template(tmpl):
  return render_template(tmpl);

# Never cache
def whats_my_ip():
  return render_template('whats_my_ip.html', client_IP=request.remote_addr)

#@layer_cache.cache()
def resume_pdf():
  result = StringIO()
  html = render_template('resume_pdf.html')
  pdf = pisa.CreatePDF(html.encode('utf8'), result)
  val = result.getvalue();
  response = Response(result.getvalue())
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'attachment; filename=BrianRBondy_Resume.pdf'
  return response;


