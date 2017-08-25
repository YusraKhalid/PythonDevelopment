from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from nltk.corpus import stopwords
from backend.news.models import News
from backend.comments.models import Comment
from backend.categories.models import Category
from backend.news.serializers.news import NewsSerializer
from backend.comments.serializers.comment import CommentSerializer
from django.db import DatabaseError
from django.db.models import Q


class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @list_route(url_path='top')
    def get_top_news(self, request):
        limit = int(request.GET.get('limit', 1))
        recent_news = News.objects.order_by('-published_date')[:limit]
        serializer = NewsSerializer(recent_news, many=True)
        return Response(serializer.data)

    @list_route(url_path='categories')
    def get_news_categories(self, request):
        limit = int(request.GET.get('limit', 1))
        categories = Category.objects.all()
        categories_news = []
        for category in categories:
            categories_news += News.objects.filter(category__name=category).order_by('-published_date')[:limit]
        serializer = NewsSerializer(categories_news, many=True)
        return Response(serializer.data)

    @list_route(url_path='search')
    def get_search_news(self, request):
        search_string = request.GET.get('query', "")
        keywords = search_string.split(' ')
        filtered_words = [word for word in keywords if word.lower() not in stopwords.words('english')]
        queries = [Q(detail__icontains=keyword) for keyword in filtered_words]
        query = queries.pop()
        for condition in queries:
            query |= condition
        searched_news = News.objects.filter(query).order_by('-published_date')
        serializer = NewsSerializer(searched_news, many=True)
        return Response(serializer.data)

    @detail_route(
                    permission_classes=[IsAuthenticated],
                    authentication_classes=[TokenAuthentication],
                    url_path='comments'
                  )
    def get_news_comments(self, request, pk=None):
        news = self.get_object()
        comments = Comment.objects.filter(news=news)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @detail_route(
                    methods=['post'],
                    permission_classes=[IsAuthenticated],
                    authentication_classes=[TokenAuthentication],
                    url_path='comment'
                )
    def post_news_comment(self, request, pk=None):
        content = request.data.get('content','')
        if content:
            news = self.get_object()
            user = request.user
            comment = Comment.objects.create(user=user, news=news, content=content)
            serializer = CommentSerializer(comment)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'content': 'this field can not be empty'})




