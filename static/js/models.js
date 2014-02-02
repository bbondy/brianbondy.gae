define(['backbone'], function(_) {

  var NewsItemModel = Backbone.Model.extend({
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
  });

  var NewsItemList = Backbone.Collection.extend({
    url: '/newsItems/',
    model: NewsItemModel
  });

  return {
    NewsItemModel: NewsItemModel,
    NewsItemList: NewsItemList
  };
});


