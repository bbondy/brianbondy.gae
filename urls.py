from app import *
import views, admin, api
from flask import redirect, url_for

####################
# View route handling

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
  return views.index(news_item_id, page, drafts, tag, recently_modified, year)

@application.route(r'/other/whatsMyIP/')
def whats_my_ip():
  return views.whats_my_ip()

@application.route(r'/resume/pdf/')
def resume_pdf():
  return views.resume_pdf()

#RSS all, or by tag
@application.route(r'/feeds/rss/')
@application.route(r'/feeds/rss/<tagged>/')
def get_rss(tagged=''):
  return views.get_rss(tagged)

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
def direct_template(tmpl):
  return views.direct_template(tmpl);

####################
# API route handling

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
def get_news_items(drafts=False, page=1, order_by=None, tag='', recently_modified=False, year=None):
  return api.get_news_items(drafts, page, order_by, tag, recently_modified, year);

@application.route(r'/newsItems/<int:id>', methods=['GET'])
def get_news_item(id):
  return api.get_news_item(id)

@application.route(r'/newsItems/<int:news_item_id>/comments')
def get_comments(news_item_id):
  return api.get_comments(news_item_id)

@application.route(r'/newsItems/<int:news_item_id>', methods=['DELETE'])
def delete_news_items(news_item_id):
  return api.delete_news_item(news_item_id)

@application.route(r'/newsItems/<int:news_item_id>', methods=['PUT'])
@application.route(r'/newsItems/', methods=['POST'])
def post_news_item(news_item_id=None):
  return api.post_news_item(news_item_id)

@application.route(r'/comments/<int:comment_id>', methods=['PUT'])
@application.route(r'/newsItems/<int:news_item_id>/comments', methods=['POST'])
def post_comment(news_item_id=None, comment_id=None):
  return api.post_comment(news_item_id, comment_id)

@application.route(r'/comments/', methods=['GET'])
def get_all_comments():
  return api.get_all_comments()

@application.route(r'/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
  return api.delete_comment(comment_id)

######################
# Admin route handling

@application.route(r'/admin/')
def admin_page():
  return admin.admin_page()

@application.route(r'/admin/newsItems/')
def admin_news_items():
  return admin.admin_news_items()

@application.route(r'/admin/newsItems/add/')
@application.route(r'/admin/newsItems/<news_item_id>/')
def admin_news_item(news_item_id = 0):
  return admin.admin_news_item(news_item_id)

@application.route(r'/admin/news_item_comments/')
def admin_news_item_comments():
  return admin.admin_news_item_comments()

@application.route(r'/admin/clear_memcache/')
def clear_memcache():
  return admin.clear_memcache()

####################
# Redirects handling

@application.route(r'/blog/')
def blog_redirect():
  return redirect(url_for('index'))

