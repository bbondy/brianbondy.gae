import os
import webapp2
from google.appengine.ext.webapp import template
import layer_cache
import ho.pisa as pisa
import cStringIO as StringIO
import logging
from blog.models import * 

#################################
class BaseHandler(webapp2.RequestHandler):
  def render_template(self, filename, **template_args):
    self.response.headers['Content-Type'] = 'text/html'
    path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    self.response.out.write(template.render(path, template_args))

#################################
class DirectTemplateHandler(BaseHandler):
  def get(self, tmpl):
    self.render_template(tmpl);

#################################
class ResumePDFHandler(BaseHandler):
  def get(self, tmpl):
    result = StringIO.StringIO()

    path = os.path.join(os.path.dirname(__file__), 'templates', 'resume_pdf.html')
    html = template.render(path, None)
    pdf = pisa.CreatePDF(html, result)
    
    self.response.headers['Content-Type'] = 'application/pdf'
    self.response.headers['Content-Disposition'] = 'attachment; filename=BrianRBondy_Resume.pdf'
    path = os.path.join(os.path.dirname(__file__), 'templates', 'resume_pdf.html')
    self.response.out.write(result.getvalue());

#################################
class WhatsMyIPHandler(BaseHandler):
  def get(self, slash):
    d = {}
    d['client_IP'] = self.request.remote_addr
    self.response.headers['Content-Type'] = 'text/html'
    path = os.path.join(os.path.dirname(__file__), 'templates', 'whats_my_ip.html')
    self.response.out.write(template.render(path, d))

#################################
class RSSHandler(BaseHandler):
  def get(self, slash, tagged=''):
    logging.error('tagged is: ' + tagged);
    rss_xml = self.getRSS(tagged)
    self.response.headers['Content-Type'] = 'application/rss+xml'
    self.response.out.write(rss_xml)
    
  @layer_cache.cache_with_key_fxn(lambda self, tagged='': ("%s" % (tagged)))
  def getRSS(self, tagged=''):
    return NewsItem.get_rss_feed(tagged)

#################################
class MainHandler(BaseHandler):
  def get(self, year = '0', recently_modified='False', drafts='False', wanted_id = '0', tagged = '', page = '1'):
    response = self.getResponse(year, recently_modified, drafts, wanted_id, tagged, page)
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(response)


  def getResponse(self, year = '0', recently_modified='False', drafts='False', wanted_id = '0', tagged = '', page = '1'):
    if drafts == 'False':
      response = self.get_cached(year, recently_modified, drafts, wanted_id, tagged, page)
      if len(response) == 0:
        return self.get_uncached(year, recently_modified, drafts, wanted_id, tagged, page)
      else:
        return response
    else:
      return self.get_uncached(year, recently_modified, drafts, wanted_id, tagged, page)

  @layer_cache.cache_with_key_fxn(lambda self, year = '0', recently_modified='False', drafts='False', wanted_id = '0', tagged = '', page = '1': "%s_%s_%s_%s_%s_%s" % (year, recently_modified, drafts, wanted_id, tagged, page))
  def get_cached(self, year = '0', recently_modified='False', drafts='False', wanted_id = '0', tagged = '', page = '1'):
    return self.get_uncached(year, recently_modified, drafts, wanted_id, tagged, page)


  def get_uncached(self, year = '0', recently_modified='False', drafts='False', wanted_id = '0', tagged = '', page = '1'):
    #Setup some initial mappings for the page based on the passed in params
    d = {}

    recently_modified=(recently_modified == 'True')
    if recently_modified:
      order_by = '-last_modified_date'
    else:
      order_by = '-posted_date'

    drafts=(drafts == 'True')
    year = int(year)
    wanted_id = int(wanted_id)
    count = 5
    page = int(page)
    page_index = page - 1
    if page < 2:
      page = 1
    if page_index < 1:
      page_index = 0
      
    #We are selecting only news items with a specific id
    if(wanted_id != 0):
      d['news_item_list'] = [NewsItem.get_by_id(wanted_id)]
      d['pagetitle'] = d['news_item_list'][0].title

    #We are selecting only news items within a certain year
    elif (year != 0):
      d['news_item_list'] = NewsItem.get_all_by_year(year, page_index, count, order_by)
      if page_index == 0:
        d['pagetitle'] = 'Blog posts for year ' + str(year)
      else:  
        d['pagetitle'] = 'Blog posts for year ' + str(year) + ' page %i' % page

    #We are selecting only news items with a specific tag
    elif  (tagged != ''):
      d['news_item_list'] = NewsItem.get_all_by_tag(tagged, page_index, count, order_by)
      if page_index == 0:
              d['pagetitle'] = "Blog posts tagged: " + tagged
      else:
              d['pagetitle'] = "Blog posts tagged: " + tagged + " page %i" % page

    #We are selecting all news items which aren't drafts
    else:
      if drafts:
        d['news_item_list'] = NewsItem.get_all_drafts(page_index, count, order_by)
      else:
        d['news_item_list'] = NewsItem.get_all(page_index, count, order_by)
      
      if recently_modified:
        if page_index == 0:
          d['pagetitle'] = 'Recently modified'
        else:
          d['pagetitle'] = 'Recently modified page %i' % page
      else:
        if page_index == 0:
          d['pagetitle'] = 'Blog'
        else:
          d['pagetitle'] = 'Blog page %i' % page


    d['archive_list'] = NewsItem.get_year_list()
    d['tag_list'] = NewsItem.get_tag_list()
    
    current_url = self.request.get('url')
    
#    current_url = request.build_absolute_uri()
    current_url = current_url.split('/page/')[0]
    if current_url[-1:] != '/':
      current_url += '/'
      
    if len(d['news_item_list']) >= count and wanted_id == 0:
      d['next_url'] = current_url + 'page/%i/' % (page+1)
    
    if page >= 2:
      d['prev_url'] = current_url +  'page/%i/' % (page-1)

    path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    return template.render(path, d)
 

"""
BLEH! TODO: rewrite this
#################################
def post_comment(request, wanted_id):
  from akismet import Akismet
  from django.utils.encoding import smart_str
  import uuid

  if request.method != 'POST':
    return http.HttpResponseRedirect('/blog')

  form = NewsItemCommentForm(request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    news_item_key = Key.from_path('NewsItem', wanted_id)
    comment.is_public = False
    comment.news_item = news_item_key

    akismet_api = Akismet(key=AKISMET_API_KEY, blog_url="http://www.brianbondy.com/")
    if akismet_api.verify_key():
      akismet_data = {
                                         'comment_type': 'comment',
                                         'referrer': request.META.get('HTTP_REFERRER', ''),
                                         'user_ip': request.META.get('REMOTE_ADDR', ''),
                                         'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'referrer':  os.environ.get('HTTP_REFERER', 'unknown'),
                                         'comment_author': smart_str(comment.name or ''),
                    'comment_author_email': smart_str(comment.email or ''),
                    'comment_author_url': smart_str(comment.homepage or ''),
                                       }
      if akismet_api.comment_check(smart_str(comment.body), akismet_data,  build_data=True):
        return http.HttpResponseRedirect('/blog/id/%s' % wanted_id)

      comment.poster_ip = request.META.get('REMOTE_ADDR', '')
    
      if not comment.email:
       comment.email = str(uuid.uuid1())

      comment.put()
      memcache.flush_all()
      from google.appengine.api import mail
      message = mail.AdminEmailMessage(sender="Brian R. Bondy <netzen@gmail.com>",
           subject="New commment posted by %s" % comment.name,
           body=comment.body)
      message.send()
  
  return http.HttpResponseRedirect('/blog/id/%s' % wanted_id)
"""
