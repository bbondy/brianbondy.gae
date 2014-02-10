/**
 * @jsx React.DOM
 */

 'use strict';

define(['models', 'react', 'showdown'], function(models, React, Showdown) {


  /**
   * Represents a list of news items
   */
  var CommentsView = React.createClass({
    getInitialState: function() {
      var comments = new models.Comments();
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
        <ul className='comments'>
          {nodes}
        </ul>
      );
    }
  });

  /**
   * Represents an individual newsItem
   */
  var CommentView = React.createClass({
    onDelete: function() {
      this.props.onDelete(this.props.comment);
    },
    onReportAsSpam: function() {
      this.props.onReportAsSpam(this.props.comment);
    },
    onReportAsGood: function() {
      this.props.onReportAsGood(this.props.comment);
    },
    render: function() {
      // This text has HTML manually stripped before it is used
      var comment = this.props.comment;
      var title = comment.get('title');
      var url = comment.get('id');

      return (
        <li>
          {comment.get('is_public') ? ' [Public]': '[NOT Public]'}
          ID: {comment.get('id')}
          <p>
            Posted By: 
            <a href={comment.get('homepage')}>{comment.get('name')} </a> (IP: {comment.get('poster_ip')})
            <br/>
            Email: {comment.get('email')}
            <br/>
            Body: {comment.get('body')}
            <br/>
            <a href='#' onClick={this.onDelete}>Delete</a> |
            <a href='#' onClick={this.onReportAsSpam}>Report as spam</a> |
            <a href='#' onClick={this.onReportAsGood}>Report as good</a>
          </p>
          <hr/>
        </li>
      );
    }
  });

  React.renderComponent(
    <CommentsView />,
    document.getElementById('comments')
  );

 return CommentsView;
});

