require.config({
  baseUrl: '/static/js/build4/',
  shim: {
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    'underscore': {
      exports: '_'
    },
    'jquery': {
      exports: '$'
    }
  },
  paths: {
    //'jquery': 'http://code.jquery.com/jquery-1.11.0.min',
    'jquery': 'jquery',
    'acorn': 'acorn',
    'codecheck': 'codecheck',
    'react': 'react',
    //'react': 'http://cdnjs.cloudflare.com/ajax/libs/react/0.8.0/react.min',
    'JSXTransformer': 'JSXTransformer',
    'showdown': 'showdown',
    //'showdown': 'http://cdnjs.cloudflare.com/ajax/libs/showdown/0.3.1/showdown.min',

    'gravatar': 'gravatar',
    'adminNewsItem': 'adminNewsItem',
    'adminNewsItems': 'adminNewsItems',

    'newsItems': 'newsItems',
    'comments': 'comments',
    'gravatar': 'gravatar',

    'backbone': 'backbone',
    //'underscore': 'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min',
    'underscore': 'underscore',
    //'backbone': 'http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.0/backbone-min',

    'models': 'models',
    'prettify': '/static/prettify/prettify',
  }
});

require(['jquery', 'underscore', 'prettify'], function($, _) {

  $(document.body).load(function () {
      $(".comments").slideUp();
  });

  function styleCode()
  {
    $("pre code").parent().each(
      function()
      {
        if(!$(this).hasClass("prettyprint"))
        {
          $(this).addClass("prettyprint");
          prettyPrint();
        }
      }
    );
  }

  function toggleAddComment(newsID)
  {
    $("#AddComment-" + newsID).slideToggle();
    $("#Comments-" + newsID).slideUp();
  }

  function toggleComments(newsID)
  {
    $("#Comments-" + newsID).slideToggle();
    $("#AddComment-" + newsID).slideUp();
  }

  function toggleTags()
  {
    $("#sidebar3").slideToggle();
          if($("#tag-label").text().indexOf(">>") != -1)
      $("#tag-label").text($("#tag-label").text().replace(">>", "<<"));
    else
      $("#tag-label").text($("#tag-label").text().replace("<<", ">>"));
  }

  $(document.links).filter(function() {
      return this.hostname != window.location.hostname;
  }).attr('target', '_blank');
});
