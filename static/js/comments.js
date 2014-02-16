/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown', 'gravatar', 'jquery'], function(models, React, Showdown, GravatarIcon) {

  var converter = new Showdown.converter();


  /**
   * Represents a view for all of the comments for a specific blog post
   */
  var CommentsView = React.createClass({
    getInitialState: function() {
      var comments = new models.Comments();
      comments.url = '/newsItems/' + this.props.newsItemId + '/comments';
      return { comments: comments };
    },

    loadFromServer: function() {
       var comments = this.state.comments;
       comments.fetch().done(function() {
         this.setState({ comments: comments });
       }.bind(this));
     },

    componentWillMount: function() {
      this.loadFromServer();
      setInterval(this.loadFromServer, 60 * 1000);
    },
    
    handleDelete: function(comment) {
      var comments = this.state.comments;
      comments.remove(comment);
      comment.destroy();
      this.setState({ comments: comments });
    },

    handleReportAsSpam: function(comment) {
      var comments = this.state.comments;
      this.setState();
      comment.set('is_public', false);
      comment.set('report_as_spam', true);
      comment.save();
      comment.unset('report_as_spam');
    },

    handleReportAsGood: function(comment) {
      var comments = this.state.comments;
      this.setState();
      comment.set('is_public', true);
      comment.set('report_as_good', true);
      comment.save();
      comment.unset('report_as_good');
    },

    render: function() {
      var self = this;
      var nodes = this.state.comments.map(function (comment) {
        return <CommentView
                 comment={comment}
                 onDelete={self.handleDelete}
                 onReportAsGood={self.handleReportAsGood}
                 onReportAsSpam={self.handleReportAsSpam}
               />;
      });
      return (
        <ul className='comments-list'>
          {nodes}
        </ul>
      );
    }
  });

  
  /**
   * Represents an individual comment 
   */
  var CommentView = React.createClass({
    render: function() {
      // This text has HTML manually stripped before it is used
      var comment = this.props.comment;
      var title = comment.get('title');
      var url = comment.get('id');

      return (
        <li className='comment-item'>
            <GravatarIcon emailHash={this.props.comment.get('emailHash')} size='60' url={comment.get('homepage')} />
            <a rel="external nofollow" href={comment.get('homepage')}>{comment.get('name')}</a> on 
            <small class="comment-date">Monday, November 18, 2013 (09:11:02)</small> says:
            <p className='comment-text'>{comment.get('body')}</p>
        </li>
      );
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
        return false;
      }
      
      var comment = new models.Comment({name: name, email: email, homepage: homepage, body: body});
      comment.url = '/newsItems/' + this.props.newsItemId + '/comments';
      comment.save().done(function(comment) {
        this.refs.name.getDOMNode().value = '';
        this.refs.email.getDOMNode().value = '';
        this.refs.homepage.getDOMNode().value = '';
        this.refs.body.getDOMNode().value = '';
        alert('Comment submitted! It will be manually reviewed and approved soon!');
      }.bind(this));
      return false;
    },
    toggleAddComment: function() {
      $('#addComment' + this.props.newsItemId).toggle()
      return false;
    },
    render: function() {
        return  <div>

          <div className='comment-controls'>
            <a href='#' onClick={this.toggleAddComment} className="comments-link">Add a new comment</a>
          </div>

          <form className='comments' style={{display: 'none'}} onSubmit={this.handleSubmit} id={'addComment' + this.props.newsItemId} method='POST'>
                 <label htmlFor='name'>Name:</label>
                 <input name='name' id='name' ref='name' placeholder='Your name' required type='text'/><br/>
                 <label htmlFor='email'>Email:</label>
                 <input placeholder='email@example.com' name='email' ref='email' id='email' required type='email'/><br/>
                 <label htmlFor='homepage'>Homepage:</label>
                 <input name='homepage' placeholder='Optional homepage' ref='homepage' id='homepage' type='url'/><br/>
                 <label htmlFor='body'>Comment:</label>
                 <textarea type='text' name='body' id='body' ref='body' placeholder='Enter your comment here, markdown accepted' required></textarea><br/>
                 <input value='Submit' type='submit'/>
          </form>
          </div>

    }
  });

 return {
   CommentsView: CommentsView,
   CommentForm: CommentForm
 };
});

