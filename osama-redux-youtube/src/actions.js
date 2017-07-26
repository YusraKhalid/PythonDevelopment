import * as youtube from "./youtubeapi";

export const SEARCH_YOUTUBE = "SEARCH_YOUTUBE";

export const searchYoutube = query => {
  return {
    type: SEARCH_YOUTUBE,
    query
  };
};

export const START_SEARCH_REQUEST = "START_SEARCH_REQUEST";
export const startSearchRequest = query => {
  return dispatch => {
    return youtube.search(query).then(jsonData => {
      dispatch(endSearchRequest(jsonData));
    });
    // .catch(error => error);
  };
};

export const END_SEARCH_REQUEST = "END_SEARCH_REQUEST";
export const endSearchRequest = jsonData => {
  return {
    type: END_SEARCH_REQUEST,
    results: jsonData.items
  };
};

export const PLAY_VIDEO = "PLAY_VIDEO";
export const playVideo = vidId => {
  return {
    type: PLAY_VIDEO,
    vidId
  };
};
