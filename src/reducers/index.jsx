import { combineReducers } from "redux";

import registerReducer from "./registerReducer";
import loginReducer from "./loginReducer";
import postReducer from "./postReducer";
import userReducer from "./userReducer";
import commentReducer from "./commentReducer";
import followingReducer from "./followingsReducer";

export default combineReducers({
  registerStatus: registerReducer,
  auth: loginReducer,
  posts: postReducer,
  users: userReducer,
  comments: commentReducer,
  followings: followingReducer
});