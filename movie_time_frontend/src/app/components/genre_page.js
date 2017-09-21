import _ from 'lodash';
import React, {Component} from 'react';
import {connect} from "react-redux";
import {Link} from "react-router-dom";
import Waypoint from 'react-waypoint';

import {MovieList} from './movies_list';
import {addToWatchlist, removeFromWatchlist} from "../actions/watchlist_actions";
import {fetchGenreMovies, fetchGenres, requestingWithGenre, loadingMore, fetchMore} from '../actions/explore_actions';
import {setActivePage} from '../actions/active_page_actions';
import {EXPLORE} from "../utils/page_types";


class GenrePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            active: null
        }
    }

    componentWillMount() {
        if (!this.props.isAuthenticated) this.props.history.push('/login/');
        this.props.setActivePage(EXPLORE);
        this.props.requestingWithGenre();
        this.props.fetchGenres();
        this.props.fetchGenreMovies(this.props.match.params.genre_id);
        this.setState({active: this.props.match.params.genre_id});
    }

    componentDidUpdate(prevProps) {
        if (this.props.match.params.genre_id !== prevProps.match.params.genre_id) {
            this.props.requestingWithGenre();
            this.props.fetchGenreMovies(this.props.match.params.genre_id);
            this.setState({active: this.props.match.params.genre_id});
        }
    }

    loadMore() {
        if(this.props.genre_movies_list.next !== null) {
            this.props.loadingMore();
            this.props.fetchMore(this.props.genre_movies_list.next);
        }
    }

    render() {
        return <div className="page-content row">
            <div className="col-md-1"/>
            <div className="col-md-8">
                <MovieList movies={this.props.genre_movies_list.movies} addToWatchlist={this.props.addToWatchlist}
                           removeFromWatchlist={this.props.removeFromWatchlist}/>
                {this.props.genre_movies_list.isFetching? <h4 className="text-center my-5">Loading...</h4>
                    : <Waypoint onEnter={this.loadMore.bind(this)} bottomOffset="-100%"/>}
            </div>
            <div className="col-md-1"/>
            <div className="col-md-2 mt-4">
                <div className="list-group position-fixed">
                    {renderGenres(this.props.genres_list, this.state.active)}
                </div>
            </div>
        </div>
    }
}

function mapStateToProps({auth_user: {isAuthenticated}, genres_list, genre_movies_list}) {
    return {isAuthenticated, genres_list, genre_movies_list};
}

const renderGenres = (genres, active) => {
    return _.map(genres, genre => {
        return (
        <Link to={`/genres/${genre.id}/movies/`} key={genre.id}
              className={`list-group-item list-group-item-action ${genre.id === parseInt(active) ? 'active' : ''}`}>
            {genre.name}</Link>);
    });
};

export default connect(mapStateToProps, {
    addToWatchlist,
    removeFromWatchlist,
    fetchGenreMovies,
    fetchGenres,
    requestingWithGenre,
    setActivePage,
    loadingMore,
    fetchMore
})(GenrePage);
