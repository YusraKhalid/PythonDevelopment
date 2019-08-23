import _ from "lodash";

import {
  FETCH_FOLLOWING,
  FOLLOW_USER,
  UNFOLLOW_USER
} from "../actions/actions.types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_FOLLOWING: {
      return {
        ...state,
        [action.payload.followerId]: indexById(action.payload.following)
      };
    }
    case FOLLOW_USER: {
      const { followerId, followeeId } = action.payload;
      const oldFollowing = state[followerId];
      const newState = {
        ...state,
        [followerId]: {
          ...oldFollowing,
          [followeeId]: true
        }
      };
      return newState;
    }
    case UNFOLLOW_USER: {
      const { followerId, followeeId } = action.payload;
      const oldFollowing = state[followerId];
      const newState = {
        ...state,
        [followerId]: {
          ..._.omit(oldFollowing, followeeId)
        }
      };
      return newState;
    }
    default:
      return state;
  }
};

const indexById = array => {
  return array.reduce((dictionary, following) => {
    dictionary[following["followeeId"]] = following["id"];
    return dictionary;
  }, {});
};
