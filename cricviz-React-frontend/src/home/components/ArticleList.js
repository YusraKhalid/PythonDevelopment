import React, {Component} from 'react';
import ArticleListItem from './ArticleListItem';

const ArticleList = (props) => {
  const AllArticles = props.articles.map((article) => {
    return (
      <ArticleListItem
        key={article.url}
        article={article} />
      );
    });

    return (
      <div>
        <ul className="col-md-8 list-group">
          {AllArticles}
        </ul>    
      </div>
    );
}


export default ArticleList;
