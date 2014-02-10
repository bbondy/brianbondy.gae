/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown', 'gravatar'], function(models, React, Showdown, Gravatar) {

  var converter = new Showdown.converter();


  /**
   * Represents a view for all of the comments for a specific blog post
   */
  var CommentsView = React.createClass({
    loadFromServer: function() {
     },

    componentWillMount: function() {
      this.loadFromServer();
      setInterval(this.loadFromServer, 60 * 1000);
    },

    render: function() {
      return <div/>
    }
  });

  /**
   * Represents a comment form to be filled out to post a comment on a blog entry
   */
  var CommentForm = React.createClass({
    handleSubmit: function() {
      var name = this.refs.name.getDOMNode().value.trim();
      var email = this.refs.email.getDOMNode().value.trim();
      var homepage = this.refs.homepage.getDOMNode().value.trim();
      var body = this.refs.body.getDOMNode().value.trim();

      var replaceHTMLExpr = /(<([^>]+)>)/ig;

      // Normally you want to filter out HTML here but this is from an authenticated trusted source
      name = name.replace(replaceHTMLExpr, '');
      email = email.replace(replaceHTMLExpr, '');
      body = body.replace(replaceHTMLExpr, '');
      homepage = homepage.replace(replaceHTMLExpr, '');
      body = body.replace(replaceHTMLExpr, '');

      if (!name || !body || !email) {
        console.log('some empty');
        return false;
      }
      
      var comment = new models.Comment({name: name, email: email, homepage: homepage, body: body});
      comment.url = '/newsItems/' + this.props.newsItemId + '/comments';
      comment.save().done(function(comment) {
        this.refs.name.getDOMNode().value = '';
        this.refs.email.getDOMNode().value = '';
        this.refs.homepage.getDOMNode().value = '';
        this.refs.body.getDOMNode().value = '';
        alert('Comment submitted!');
      }.bind(this));
      return false;
    },
    render: function() {
        return  <div>

          <div className='comment-controls'>
            <a href="Javascript:toggleAddComment(156);" className="comments-link">Add a new comment</a> | 
            <a href="Javascript:toggleComments(156);" classNmae="comments-link">2 comment(s)</a>
          </div>

          <form className='comments' onSubmit={this.handleSubmit} method='POST'>
                 <label htmlFor='name'>Name:</label>
                 <input name='name' id='name' ref='name' placeholder='Your name' required='' type='text'/><br/>
                 <label htmlFor='email'>Email:</label>
                 <input placeholder='email@example.com' name='email' ref='email' id='email' required='' type='email'/><br/>
                 <label htmlFor='homepage'>Homepage:</label>
                 <input name='homepage' placeholder='Optional homepage' ref='homepage' id='homepage' type='url'/><br/>
                 <label htmlFor='body'>Comment:</label>
                 <textarea type='text' name='body' id='body' ref='body' placeholder='Enter your comment here, markdown accepted' required=''></textarea><br/>
                 <input value='Submit' type='submit'/>
                 <p>Comments will be manually verified after automated filtering and will show up within 24h</p>
          </form>
          </div>

    }
  });

 return {
   CommentsView: CommentsView,
   CommentForm: CommentForm
 };
});

