import React, { Component } from "react";
import { connect } from "react-redux";
import moment from "moment";

import history from "../../history";
import AddComment from "../AddComment/AddComment";
import CommentList from "../CommentList/CommentList";

import { deletePost } from "../../actions/post.actions";

import "./Post.sass";

class Post extends Component {
  state = { showComments: false, description: "View comments" };

  toggleComments = () => {
    this.setState({
      showComments: !this.state.showComments,
      description: this.state.showComments ? "View comments" : "Hide comments"
    });
  };

  renderComments = () => {
    if (this.state.showComments)
      return <CommentList postId={this.props.post.id} />;
  };

  handleDeletePost = postId => {
    this.props.deletePost(postId);
  };

  renderUserName = user_id => {
    const user = this.props.users[user_id];
    if (user) {
      return `${user.first_name} ${user.last_name}`;
    }
    return "...";
  };

  renderUserPicture = user_id => {
    const user = this.props.users[user_id];
    if (user) {
      return (
        <img className="profile-picture" src={user.display_picture} alt="" />
      );
    }
    return "...";
  };

  renderDate(date) {
    if (
      moment(date)
        .add(3, "hours")
        .isBefore()
    )
      return moment(date).format("MMMM D [at] h[:]m A");
    else return moment(date).fromNow();
  }

  renderAddComment = postId => {
    if (this.props.auth.isSignedIn)
      return (
        <AddComment
          postId={postId}
          showComments={() => {
            this.setState({
              showComments: true,
              description: "Hide comments"
            });
          }}
        />
      );
  };

  renderCross = (postId, authorId) => {
    if (
      this.props.auth.isSignedIn &&
      authorId === parseInt(this.props.auth.user_id)
    ) {
      return (
        <button
          onClick={() => this.handleDeletePost(postId)}
          type="button"
          className="close"
        >
          <span aria-hidden="true">&times;</span>
        </button>
      );
    }
    return null;
  };

  renderPostMedia = media => {
    if (media.length > 0) {
      return (
        <div className="post-media">
          {media.map((image, i) => (
            <img key={i} className="images" src={image} alt="#"></img>
          ))}
        </div>
      );
    }
    return null;
  };

  renderPost = post => {
    return (
      <div className="Post">
        <div className="card">
          {this.renderCross(post.id, post.author)}
          <div className="meta">
            <div>{this.renderUserPicture(post.author)}</div>
            <div className="name-time">
              <div
                onClick={() => {
                  history.push(`/user/${post.author}`);
                }}
                className="profile-link"
              >
                {this.renderUserName(post.author)}
              </div>
              <div className="time">{this.renderDate(post.time)}</div>
            </div>
          </div>
          <div className="post-status">{post.status}</div>
          {this.renderPostMedia(post.media)}
          <div className="comments-toggle">
            <div onClick={this.toggleComments}>{this.state.description}</div>
          </div>
        </div>
        {this.renderComments()}
        {this.renderAddComment(post.id)}
      </div>
    );
  };

  render = () => {
    return this.renderPost(this.props.post);
  };
}

const mapStateToProps = state => {
  return { users: state.users, auth: state.auth };
};

export default connect(
  mapStateToProps,
  { deletePost }
)(Post);