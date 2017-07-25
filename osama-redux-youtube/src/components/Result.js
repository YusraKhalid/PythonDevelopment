import React from "react";
import PropTypes from "prop-types";
import "./Result.css";

class Result extends React.Component {
  render() {
    return (
      <div className="result">
        <img
          className="thumbnail"
          src={this.props.imgurl}
          alt={this.props.title}
        />
        <div className="detail">
          <h3 className="title">
            {this.props.title}
          </h3>
          <p className="description">
            {this.props.description}
          </p>
        </div>
      </div>
    );
  }
}

Result.PropTypes = {
  imgurl: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string
};

export default Result;
