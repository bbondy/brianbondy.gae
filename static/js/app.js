require.config({
  baseUrl: '/static/js',
  paths: {
    //'jquery': 'http://code.jquery.com/jquery-1.11.0.min',
    'jquery': 'jquery',
    'underscore': 'underscore-min',
    'acorn': 'acorn',
    'codecheck': 'codecheck',
    'analytics': 'analytics',
    'react': 'react-0.8.0',
    'JSXTransformer': 'JSXTransformer',
    'showdown': 'showdown-0.3.1',
    //'showdown': 'http://cdnjs.cloudflare.com/ajax/libs/showdown/0.3.1/showdown.min',

    'gravatar': 'gravatar',
    'adminNewsItem': 'adminNewsItem',
    'adminNewsItems': 'adminNewsItems',

    'newsItems': 'newsItems',

    'backbone': 'backbone-1.1.0',
    //'backbone': 'http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.0/backbone-min',


    'models': 'models',
    'prettify': '/static/prettify/prettify',
    'plusone': 'https://apis.google.com/js/plusone'
  }
});

require(['analytics', 'jquery', 'underscore', 'prettify'], function() {

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
