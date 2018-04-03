import postApi from '../api/post';
import {getAllPostsSuccess ,getAllPostsFailed,getPostSuccess,getPostFailed,
    addPostSuccess, addPostFailed, updatePostSuccess, updatePostFailed,
    deletePostSuccess,deletePostFailed,LoadPostsProgress} from './index';
import commentApi from '../api/comment';

export function loadAllPosts() {

    return function(dispatch) {
        dispatch(LoadPostsProgress());

        postApi.getAllPostsData().then(posts => {
            dispatch(getAllPostsSuccess(posts));

        }).catch(error => {

            dispatch(getAllPostsFailed(error));
        });
    }
}
export function loadPost(postId) {

    return function(dispatch) {

        postApi.getPost(postId).then(post => {
            if(post.commentCount>0){
                commentApi.getComments(postId).then(comments =>{

                    dispatch(getPostSuccess(post, comments));

                }).catch(error => {
                    dispatch(getPostFailed(error));
                })
            }else{
                dispatch(getPostSuccess(post, []));

            }

        }).catch(error => {

            dispatch(getPostFailed(error));
        });
    }
}
export function addPost(post) {

    post.timestamp=Date.now();
    return function(dispatch) {

        postApi.addPost(post).then(response => {
            dispatch(addPostSuccess(response));

        }).catch(error => {

            dispatch(addPostFailed(error));
        });
    }
}
export function editPost(post) {

    return function(dispatch) {

        postApi.editPost(post, post.id).then(response => {
            dispatch(updatePostSuccess(response, post.id));

        }).catch(error => {

            dispatch(updatePostFailed(error));
        });
    }

}
export function deletePost(postId) {
    return function(dispatch) {

        postApi.deletePost(postId).then(response => {
            dispatch(deletePostSuccess(response, postId));

        }).catch(error => {

            dispatch(deletePostFailed(error));
        });
    }
}
