from blog.models import NewsItem, NewsItemComment
from google.appengine.ext.db import djangoforms

class NewsItemForm(djangoforms.ModelForm):
	class Meta:
		model = NewsItem

class NewsItemCommentForm(djangoforms.ModelForm):
	class Meta:
		model = NewsItemComment
