from rest_framework import permissions
from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet
from web.posts.models import Post
from web.posts.serializers.post_serializer import PostSerializer


class NewPostViewSet(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

