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

  return {
    NewsItem: NewsItem,
    NewsItems: NewsItems
  };
});


