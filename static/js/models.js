define(['backbone'], function(_) {

  var NewsItem = Backbone.Model.extend({
    urlRoot: '/newsItems/',
    initialize: function() {
    },
    defaults: {
      title: '',
      body: '',
      tags: [],
      posted_date: new Date(),
      last_modified_date: new Date(),
      draft: true
    },
    tagsStr: function() {
      return this.get('tags').join(', ');
    },
  });

  var NewsItems = Backbone.Collection.extend({
    url: '/newsItems/',
    model: NewsItem
  });

  var Comment = Backbone.Model.extend({
    urlRoot: '/comments/',
    initialize: function() {
    },
    defaults: {
      name: '',
      homepage: '',
      email: '',
      body: '',
      posted_date: new Date(),
    },
  });

  var Comments = Backbone.Collection.extend({
    url: '/comments/',
    model: Comment
  });

  return {
    NewsItem: NewsItem,
    NewsItems: NewsItems,
    Comment: Comment,
    Comments: Comments
  };
});




