from google.appengine.ext import db
import datetime
import markdown
from libs import PyRSS2Gen
import logging
import md5
import layer_cache
from google.appengine.api import memcache

class BaseModel(db.Model):
  pass

class Tag(BaseModel):
  tag = db.StringProperty()

class NewsItem(BaseModel):#Which in turn dervies from GAE's db.Model
  title = db.StringProperty()
  body = db.TextProperty()
  posted_date = db.DateTimeProperty(auto_now_add=True)
  last_modified_date = db.DateTimeProperty(auto_now=True)
  draft = db.BooleanProperty(default=True)
  _KEY_PREFIX = 'NewsItem'
  
  def getJSONData(self):
    return { 'id': self.id(),
             'title': self.title,
             'body': self.body,
             'posted_date': str(self.posted_date),
             'last_modified_date': str(self.last_modified_date),
             'draft': self.draft,
             'tags':  [i.tag.tag for i in self.tags]
  }
  jsonData = property(getJSONData)


  def clearTags(self):
    #Delete any associated tags so far
    tag_rels_to_del = NewsItemTag.all() \
        .filter('news_item', self.key())
    for tag_rel in tag_rels_to_del:
      tag_rel.delete()

  @staticmethod
  def create():
    return NewsItem(key_name=NewsItem.get_next_unique_id())
  
  #we use unique integer IDs to keep it consistent with the old 
  # IDs so we don't break old URLs and new consistency
  @staticmethod
  def get_next_unique_id():
    q = db.Query(NewsItem, keys_only=False).order("-posted_date")
    result = q.fetch(1)
    if len(result) == 0:
      return "1"
    else:
      return str(int(result[0].key().name()) + 1)

  def id(self):
    return self.key().name()

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return "/blog/id/" + str(self.id)
    
  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda id: "%s" % id)
  def get_by_id(id):
    key = db.Key.from_path('NewsItem', str(id))
    news_item = NewsItem.all() \
    .filter('draft', False) \
    .filter('__key__', key).get()
    news_item.add_meta_fields()
    return news_item
  
  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda year, page_index, count, order_by: "%s_%s_%s_%s" % (year, page_index, count, order_by))
  def get_all_by_year(year, page_index, count, order_by):
    news_items = NewsItem.all()  \
      .filter('posted_date >=', datetime.datetime(year,1,1,0,0)) \
      .filter('posted_date <=', datetime.datetime(year,12,31,23,59,59)) \
      .filter('draft', False) \
      .order(order_by) \
      .fetch(count, page_index*count)
    for news_item in news_items:
      news_item.add_meta_fields()
    return news_items

  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda tag, page_index, count, order_by: "%s_%s_%s_%s" % (tag, page_index, count, order_by))
  def get_all_by_tag(tag, page_index, count, order_by):
    tags = Tag.all().filter('tag', tag).order('tag')
    
    tag_ni = tags.get().news_items.fetch(count,page_index*count)
    news_items = [t.news_item for t in tag_ni if not t.news_item.draft]
    news_items.sort(reverse=True, key=lambda x: x.posted_date)
    for news_item in news_items:
      news_item.add_meta_fields()
    return news_items
  

  @staticmethod
  def get_all_drafts(page_index, count, order_by):
    news_items = NewsItem.all() \
      .filter('draft', True) \
      .order(order_by)[page_index*count:page_index*count+count]

    for news_item in news_items:
      news_item.add_meta_fields()
    return news_items
      

  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda page_index, count, order_by: ("%s_%s_%s" % (page_index, count, order_by)))
  def get_all(page_index, count, order_by):
    news_items = NewsItem.all() \
      .filter('draft', False) \
      .order(order_by)[page_index*count:page_index*count+count]
    
    for news_item in news_items:
      news_item.add_meta_fields()
    
    return news_items
  
  @staticmethod
  @layer_cache.cache()
  def get_tag_list():
    tag_list = [(tag.tag, tag.news_items.count()) for tag in Tag.all()]
    return tag_list
  
  def add_meta_fields(self):
    self._linkback =  "http://www.brianbondy.com/blog/id/" + self.key().name() + "&title=" + self.title
    self._delicious_link = "http://del.icio.us/post?url="
    self._digg_link = "http://digg.com/submit?phase=2&url="
    self._twitter_link = "http://twitter.com/?status="
    self._facebook_link = "http://www.facebook.com/sharer.php?u="
    self._sorted_comments = self.comments.filter('is_public', True).order('posted_date').fetch(100, 0)
    self._markdown_body = markdown.markdown(self.body)
    
  def linkback(self):
    return self._linkback
  def delicious_link(self):
    return self._delicious_link
  def digg_link(self):
    return self._digg_link
  def twitter_link(self):
    return self._twitter_link
  def facebook_link(self):
    return self._facebook_link
  def sorted_comments(self):
    return self._sorted_comments
  def markdown_body(self):
    return self._markdown_body
  
  @staticmethod
  @layer_cache.cache()
  def get_year_list():
    if NewsItem.all().count() != 0:
      oldest_year = NewsItem.all().order('posted_date') \
        .fetch(1)[0].posted_date.year
      newest_year = NewsItem.all().order('-posted_date') \
        .fetch(1)[0].posted_date.year
      years = range(int(newest_year), int(oldest_year)-1, -1)
    else:
      years = [datetime.datetime.now().year]
    year_list = list(years)
    return year_list


  @staticmethod
  @layer_cache.cache()
  def get_count():
    return NewsItem.all(keys_only=True).count()
    
  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda tagged='': ("%s" % (tagged)))
  def get_rss_feed(tagged=''):
    rss = PyRSS2Gen.RSS2(
      title = "Brian R. Bondy's Feed",
      link = "http://www.brianbondy.com/blog/",
      description = "Blog posts by Brian R. Bondy",
      lastBuildDate = datetime.datetime.utcnow(),
      items = []
    )

    count_to_get = 30
    if(tagged == ''):
      news_list = NewsItem.all() \
        .filter('draft', False) \
        .order('-posted_date')[:count_to_get]
    else:
      news_list = NewsItem.get_all_by_tag(tagged, 0, count_to_get, '-posted_date')

    for news in news_list:
      #url_link = "http://www.brianbondy.com/blog/id/1",# % news.id(),
  
      rss.items.append(
        PyRSS2Gen.RSSItem(
          title = news.title,
          link = "http://www.brianbondy.com/blog/id/" + str(news.id()),
          description = markdown.markdown(news.body),
          guid = PyRSS2Gen.Guid("http://www.brianbondy.com/blog/id/" + str(news.id())),
          pubDate = news.posted_date
        )
      )
    
    rss_xml = rss.to_xml()
    return rss_xml
  

class NewsItemTag(BaseModel):
  tag = db.ReferenceProperty(Tag, collection_name='news_items')  
  news_item = db.ReferenceProperty(NewsItem, collection_name='tags')

class NewsItemComment(BaseModel):
  news_item = db.ReferenceProperty(NewsItem, collection_name='comments')
  name = db.StringProperty()
  homepage = db.StringProperty()
  email = db.StringProperty()
  body = db.TextProperty()
  posted_date = db.DateTimeProperty(auto_now_add=True)
  poster_ip = db.StringProperty()
  is_public = db.BooleanProperty(default=True)

  def id(self):
    return self.key().id() or self.key().name()

  def getEmailHash(self):
    m = md5.new()
    m.update(self.email.strip().lower())
    return m.hexdigest()

  def getAllJSONData(self):
    return { 'id': self.id(),
             'name': self.name,
             'homepage': self.homepage,
             'email': self.email,
             'emailHash': self.getEmailHash(),
             'body': self.body,
             'posted_date': str(self.posted_date),
             'news_item_id': str(self.news_item.id()),
             'is_public': self.is_public,
             'poster_ip': self.poster_ip
           }
  allJSONData = property(getAllJSONData)

  def getJSONData(self):
    return { 'id': self.id(),
             'name': self.name,
             'homepage': self.homepage,
             'emailHash': self.getEmailHash(),
             'body': self.body,
             'posted_date': str(self.posted_date),
             'news_item_id': str(self.news_item.id()),
             'is_public': self.is_public,
           }
  jsonData = property(getJSONData)

  @staticmethod
  def create():
    return NewsItemComment()

  @staticmethod
  @layer_cache.cache_with_key_fxn(lambda id: "%s" % id)
  def get_by_id(id):
    key = db.Key.from_path('NewsItemComment', id)
    return NewsItemComment.get(key)
