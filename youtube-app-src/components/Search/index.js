import React from 'react';
import { BRAND_NAME, SEARCH_BUTTON } from '../../shared/copies.js';

const Search = ({ onClick }) => {
  return (
    <nav className="navbar navbar-light bg-light search-panel">
      <label className="navbar-brand">{BRAND_NAME}</label>
      <div className="form-inline">
        <input
          className="form-control mr-sm-2"
          type="text"
          placeholder="Search"
          aria-label="Search"
          id="searchInput"
        />
        <button
          className="btn btn-outline-success my-2 my-sm-0"
          onClick={() => {
            onClick();
          }}
        >
          {SEARCH_BUTTON}
        </button>
      </div>
    </nav>
  );
};

export default Search;
