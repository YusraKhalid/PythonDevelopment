import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from . import models


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


class ListPosts(ListView):

    model = models.Post
    context_object_name = 'posts'
    # queryset = models.Post.objects.all()
    template_name = 'blog/list_display.html'

    def get_queryset(self):
        filter_on = self.request.GET.get('search')
        if filter_on:
            new_context = models.Post.objects.filter(
                title=filter_on,
            )
        else:
            new_context = models.Post.objects.all()

        return new_context


class CreatePost(LoginRequiredMixin, ListView):

    model = models.Category
    context_object_name = 'categories'
    queryset = models.Category.objects.all()
    template_name = 'blog/create_post.html'

    def post(self, request, *args, **kwargs):
        post = models.Post(title=request.POST.get('title'), body=request.POST.get('body'), author=request.user,
                           modified_at=datetime.now(), category_id=request.POST.get('category'))
        post.save()

        return redirect('/blog/post/listposts/')


class ViewPost(LoginRequiredMixin, DetailView):

    model = models.Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(ViewPost, self).get_context_data(**kwargs)
        post = context['post']
        comment_body = post.comments.all()
        comment_likes = [likes for _, likes in post.comment_likes().items()]
        comment = zip(comment_body, comment_likes)
        context['comments'] = comment
        context['like_post'] = post.post_likes()

        return context

    def post(self, request, **kwargs):
        vote_choice = {'up_vote': 1, 'down_vote': -1}
        post_id = kwargs.get('pk')

        if request.POST.get('vote'):
            vote = request.POST.get('vote')
            vote = vote_choice[vote]
            models.LikePost.objects.create(created_at=datetime.now(), post_id=post_id, user_id=1, vote=vote)

        else:
            vote = request.POST.get('commentvote')
            comment_id = request.POST.get('comment_id')
            vote = vote_choice[vote]
            models.LikeComment.objects.create(created_at=datetime.datetime.now(), comment_id=comment_id, user_id=1, vote=vote)

        return redirect('/blog/post/id/{}/'.format(post_id))
