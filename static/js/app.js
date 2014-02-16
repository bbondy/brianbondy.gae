require.config({
  baseUrl: '/static/js',
  paths: {
    'jquery': 'http://code.jquery.com/jquery-1.11.0.min',
    //'jquery': 'jquery-1.11.0.js',
    'acorn': 'acorn',
    'codecheck': 'codecheck',
    'react': 'react-0.8.0',
    'JSXTransformer': 'JSXTransformer',
    //'showdown': 'showdown-0.3.1',
    'showdown': 'http://cdnjs.cloudflare.com/ajax/libs/showdown/0.3.1/showdown.min',

    'gravatar': 'gravatar',
    'adminNewsItem': 'adminNewsItem',
    'adminNewsItems': 'adminNewsItems',

    'newsItems': 'newsItems',
    'comments': 'comments',
    'gravatar': 'gravatar',

    //'backbone': 'backbone-1.1.0',
    'underscore': 'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min',
    //'underscore': 'underscore-min'
    'backbone': 'http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.0/backbone-min',

    'models': 'models',
    'prettify': '/static/prettify/prettify',
  }
});

require(['underscore', 'jquery', 'prettify'], function() {

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
