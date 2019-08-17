import React, { Component } from "react";
import NewPost from "../NewPost/NewPost";
import Feed from "../Feed/Feed";
import Sidebar from "../Sidebar/Sidebar";
import Topbar from "../Topbar/Topbar";

import "./Home.css";

class Home extends Component {
  state = {};

  render = () => {
    return (
      <>
        <Topbar />
        <Sidebar />
        <div className="container" id="main-container">
          <div className="main">
            <NewPost />
            <Feed />
          </div>
        </div>
      </>
    );
  };
}

export default Home;
