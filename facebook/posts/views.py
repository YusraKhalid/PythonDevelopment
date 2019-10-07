from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post

from .forms import CreatePostForm


@login_required
def post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.fb_user = request.user
            new_post.save()
            # resetting the from
            form = CreatePostForm()
    else:
        form = CreatePostForm()
    posts = Post.objects.all().order_by("id").reverse()
    return render(request, 'home.html', {'form': form, 'posts' : posts})