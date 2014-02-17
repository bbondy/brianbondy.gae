/**
 * @jsx React.DOM
 */

 'use strict';

define(['jquery', 'models', 'react', 'showdown', 'comments'], function($, models, React, Showdown, commentCtrls) {

  var converter = new Showdown.converter();
  var CommentsView = commentCtrls.CommentsView;
  var CommentForm = commentCtrls.CommentForm;


  /**
   * Represents a view for the tag items
   */
  var TagsView = React.createClass({
    render: function() {
      var nodes = this.props.tags.map(function (tag) {
        var tagURL = '/blog/tagged/' + tag;
        return <a href={tagURL} className='post-tag' rel='tag'>{tag}</a>  
      });
      return (
        <p> Tags:
          {nodes}
        </p>
      );
    }
  });

  /**
   * Represents a list of news items
   */
  var NewsItemsView = React.createClass({
    getInitialState: function() {
      var newsItems = new models.NewsItems();
      if (drafts) {
        newsItems.url += 'drafts/';
      } else if (tag) {
        newsItems.url += 'tagged/' + tag + '/';
      } else if (year && recentlyModified) {
        newsItems.url += 'modified/' + year + '/';
      } else if (year) {
        newsItems.url += 'posted/' + year + '/';
      } else if (recentlyModified) {
        newsItems.url += 'modified/recent/';
      }

      if (page) {
        newsItems.url += 'page/' + page;
      }

      if (count) {
        newsItems.url += '?count=' + count;
      }

      return { newsItems: newsItems };
    },

    loadFromServer: function() {
       var newsItems = this.state.newsItems;
       newsItems.fetch().done(function() {
         this.setState({ newsItems: newsItems });
       }.bind(this));
     },

    componentWillMount: function() {
      this.loadFromServer();
      setInterval(this.loadFromServer, 60 * 1000);
    },

    render: function() {
      var nodes = this.state.newsItems.map(function (newsItem) {
        return <NewsItemView
                 newsItem={newsItem}
               />;
      });
      return (
        <div className='newsItems'>
          {nodes}
        </div>
      );
    }
  });

  function slugify(str) {
   return str.toLowerCase().replace(/ /g,'-').replace(/[^\w-]+/g,'');
  }

  /**
   * Represents an individual newsItem
   */
  var NewsItemView = React.createClass({
    getInitialState: function() {
      if (this.props.newsItem) {
        return { newsItem : this.props.newsItem, preloaded : true}
      } else {
        return { newsItem: new models.NewsItem({'id': newsItemId}) }
      }
    },
    componentWillMount: function() {
      if (this.state.preloaded)
        return;
      var n1 = this.state.newsItem;
      n1.fetch().done(function(ni) {
        this.setState({ newsItem: new models.NewsItem(ni) });
      }.bind(this));
    },

    render: function() {

      var n = this.state.newsItem;

      // This text has HTML manually stripped before it is used
      var title = n.get('title');
      var url = '/blog/id/' + n.get('id') + '/' + slugify(n.get('title'));
      var postedDate = n.get('posted_date');
      if (_.isString(postedDate)) { 
        postedDate = new Date(Date.parse(n.get('posted_date').split(' ')[0]));
      }
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var postedMonth = months[postedDate.getMonth()];
      var rawBody = converter.makeHtml(n.get('body'));
      var lastModifiedDate = n.get('last_modified_date');
      if (_.isString(lastModifiedDate)) {
        lastModifiedDate = new Date(Date.parse(n.get('last_modified_date').split(' ')[0]));
      }
      var lastModifiedTime = lastModifiedDate.getHours() + ':' + lastModifiedDate.getMinutes() + ':' + lastModifiedDate.getSeconds();
      var lastModifiedMonth = months[lastModifiedDate.getMonth()];
      var lastModifiedStr = lastModifiedMonth + ' ' + lastModifiedDate.getDate() + ' ' + lastModifiedDate.getFullYear();

      return (

        <div id='post'>
          <div id='post-date'>
            <div id='post-month'>
              <span>{postedMonth}</span>
            </div>
            <div id='post-day'>
              <span>{postedDate.getDate()}</span>
            </div>
            <div id='post-year'>
              <span>{postedDate.getFullYear()}</span>
            </div>
          </div>

          <div id='post-content'>
            <h2><a href={url}>{n.get('title')}</a></h2>

            <h3>
              Last modified: {lastModifiedStr}
            </h3>

            <div className='bold-divider'></div>

            <div className='blog-body'>
               <p dangerouslySetInnerHTML={{__html: rawBody}} />
            </div>

            <TagsView tags={n.get('tags')}/>
            <CommentForm newsItemId={n.get('id')}/>
            <CommentsView newsItemId={n.get('id')}/>
          </div>


        </div>
      );
    }

  });

  if (newsItemId) {
    React.renderComponent(
      <NewsItemView newsItemId={newsItemId} />,
      document.getElementById('news-items')
    );
  } else {
    React.renderComponent(
      <NewsItemsView />,
      document.getElementById('news-items')
    );
  }

 return NewsItemsView;
});

