from django.contrib import admin
from brianbondy.blog.models import *

#admin.site.register(NewsItem)


class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'posted_date', )
	list_filter = ('posted_date', 'draft',)
	date_hierarchy = 'posted_date'
	ordering = ('-posted_date', )

admin.site.register(NewsItem, BlogAdmin)
