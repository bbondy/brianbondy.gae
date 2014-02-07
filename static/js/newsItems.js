/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown'], function(models, React, Showdown) {


  /**
   * Represents a list of news items
   */
  var NewsItemsView = React.createClass({
    getInitialState: function() {
      return { newsItems: new models.NewsItems() };
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
        <ul className='newsItems'>
          {nodes}
        </ul>
      );
    }
  });

  /**
   * Represents an individual newsItem
   */
  var NewsItemView = React.createClass({
    render: function() {
      // This text has HTML manually stripped before it is used
      var title = this.props.newsItem.get('title');
      var url = '/admin1/newsItems/' + this.props.newsItem.get('id');

      return (
        <li>
          <a href={url}>
            {this.props.newsItem.get('id')} : {this.props.newsItem.get('title')}
          </a>
        </li>
      );
    }
  });

  React.renderComponent(
    <NewsItemsView />,
    document.getElementById('news-items')
  );

 return NewsItemsView;
});
