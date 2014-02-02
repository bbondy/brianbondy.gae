/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown'], function(models, React, Showdown) {


  console.log('hi');
  var NewsItemModel = models.NewsItemModel;
  var converter = new Showdown.converter();

  /**
   * The HTML form for filling out the blog post
   */
  var NewsItemForm = React.createClass({
    handleSubmit: function() {
      var body = this.refs.body.getDOMNode().value.trim();
      var tagsStr = this.refs.tags.getDOMNode().value.trim();
      var draft = this.refs.draft.getDOMNode().checked;
      body = body.replace(/(<([^>]+)>)/ig,'');
      if (!body) {
        return false;
      }
      var newsItem = new NewsItemModel({body: body, tags: tagsStr.split(',')});
      newsItem.draft = draft;
      newsItem.save();
      this.refs.body.getDOMNode().value = '';
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
    },
    render: function() {
      return (
        <form className='NewsItemForm' onSubmit={this.handleSubmit}>
          <textarea className='newsItem' rows='6' cols='200' placeholder='Blog post in markdown here!' ref='body' />
          <br/>
          <label for='id_tags' className='newsItem'>Tags:</label>
          <input className='newsItem' type='text' name='tags' id='id_tags' ref='tags' size='60' placeholder='Comma separated list of tags here'/>
          <input className='newsItem' type='checkbox' ref='draft' checked>Draft</input>
          <input className='newsItem' type='submit' name='submit' value='Save Continue' onSubmit={this.handleSaveAndContinue}/>
          <input classname='newsItem' type='submit' name='submit' value='Save Done' onSubmit={this.handleSaveAndDone}/>
          <input className='newsItem' type='submit' name='submit' value='Delete' onSubmit={this.handleDelete}/>
        </form>
      );
    }
  }); 



  React.renderComponent(
    <NewsItemForm />,
    document.getElementById('news-item-form')
  );

 return NewsItemForm;
});

