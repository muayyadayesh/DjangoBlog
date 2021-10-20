from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
from django.utils import timezone
# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

#list of posts in a listview
class PostListView(ListView):
     model = Post
     def get_queryset(self):
         #lte = Less than or equal to
         # -,+ : descending, ascending
         return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')


#post details
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'

#create a new post using createview
class CreatePostView(LoginRequiredMixin, CreateView):

    form_class = PostForm
    model = Post

    login_url = '/login'
    redirect_field_name = 'app/post_details.html'


#update a post uisng updateview
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'app/post_details.html'

    form_class = PostForm
    model = Post

#delete post using deleteview
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('app:post_list')

#list drafts - listview
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'app/post_details.html'

    model = Post

    def get_queryset(self):
         #lte = Less than or equal to
         # -,+ : descending, ascending
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#publish drafted post
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('app:post_details', pk=pk)

#add a comment to post
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(data= request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('app:post_details', pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'app/comment_form.html', {'form': form})

#approve a comment
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk= pk)
    comment.approve()
    return redirect('app:post_details', pk=comment.post.pk)


#remove a comment
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk= pk)
    post_pk = comment.post.pk
    comment.delete()
    redirect('app:post_details', pk=post_pk)
