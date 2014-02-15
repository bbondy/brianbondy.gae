/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown'], function(models, React, Showdown) {


  var converter = new Showdown.converter();

  /**
   * The HTML form for filling out the blog post
   */
  var NewsItemForm = React.createClass({
     getInitialState: function() {
      if (newsItemId) {
        return { newsItem: new models.NewsItem( { id: newsItemId }) };
      } else {
        return { newsItem: new models.NewsItem() };
      }
    },

    loadFromServer: function() {
       if (newsItemId) {
         var newsItem = this.state.newsItem;
         newsItem.fetch({ data: $.param({ uncached: 1}) }).done(function() {
           this.setState({ newsItem: newsItem });
         }.bind(this));
       }
     },

    componentWillMount: function() {
      this.loadFromServer();
      setInterval(this.loadFromServer, 60 * 1000);
    },

    handleSubmit: function(event) {
      event.preventDefault();
      var title = this.refs.title.getDOMNode().value.trim();
      var body = this.refs.body.getDOMNode().value.trim();
      var tagsStr = this.refs.tags.getDOMNode().value.trim();
      var draft = this.refs.draft.getDOMNode().checked;
      // Normally you want to filter out HTML here but this is from an authenticated trusted source
      //body = body.replace(/(<([^>]+)>)/ig,'');
      //title = title.replace(/(<([^>]+)>)/ig,'');
      if (!title || !body) {
        return false;
      }
      this.state.newsItem.set({body: body, title: title, tags: tagsStr.split(','), draft: draft});
      this.state.newsItem.save().done(function(newsItem) {
        alert('saved!');
      }.bind(this));
      return false;
    },
    handleSaveAndContinue: function() {
      this.handleSubmit();
      return false;
    },
    handleSaveAndDone: function() {
      this.handleSubmit();
      return false;
    },
    handleDelete: function() {
      if (!confirm('Are you sure you want to remove this blog post completely?')) {
        return;
      }
      this.state.newsItem.destroy().done(function() {
        location.href = '/admin/newsItems/';
      }.bind(this));
    },
    handleChange: function(event) {
      var id = event.target.id;
      var val = event.target.value;
      if (id === 'draft')
        val = event.target.checked;
      this.state.newsItem.set(id, val);
      this.setState({ });
    },
    render: function() {
      return (
        <div>
        <form className='NewsItemForm' onSubmit={this.handleSubmit}>
          <input className='newsItem' type='text' id='title' ref='title' size='60' placeholder='Title of the blog post' value={this.state.newsItem.get('title')} onChange={this.handleChange} />
          <textarea className='newsItem' rows='6' cols='200' placeholder='Blog post in markdown here!' ref='body' id='body' value={this.state.newsItem.get('body')} onChange={this.handleChange} />
          <br/>
          <label htmlFor='tags' className='newsItem'>Tags:</label>
          <input className='newsItem' type='text' id='tags' ref='tags' size='60' placeholder='Comma separated list of tags here' value={this.state.newsItem.tagsStr()} onChange={this.handleChange} />
          <input className='newsItem' type='checkbox' id='draft' ref='draft' checked={this.state.newsItem.get('draft')} onChange={this.handleChange}>Draft</input>
          <p>
          <a href='#' onClick={this.handleSubmit}>Save and continue</a> | <a href='#' onClick={this.handleDelete}>Delete</a>
          </p>
        </form>
        <br/>
        <p><a href='/admin/newsItems/'>Back to News Items</a></p>
        </div>
      );
    }
  }); 



  React.renderComponent(
    <NewsItemForm />,
    document.getElementById('news-item-form')
  );

 return NewsItemForm;
});

