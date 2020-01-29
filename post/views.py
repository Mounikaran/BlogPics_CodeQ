from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from braces.views import FormValidMessageMixin

from post.models import Post, Comment
from post.forms import PostForm, CommentForm


class PostList(generic.ListView):
    model = Post
    #form_classes = {'post_form' : PostForm, 'comment_form' : CommentForm}
    template_name = 'post/post_list.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

class DeletePost(LoginRequiredMixin, FormValidMessageMixin, generic.DeleteView):
    template_name = 'post/confirm_delete.html'
    model = Post
    success_url = reverse_lazy('post:postlist')
    form_valid_message = 'Post Deleted Successfully'

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])

        if (post.post_user != request.user):
            return HttpResponseRedirect(reverse_lazy('post:postdetail', kwargs={'slug': kwargs['slug']}))
        else:
            return super(DeletePost, self).get(request, *args, **kwargs)

class UploadPost(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post/post_form.html'
    success_url = reverse_lazy('post:postlist')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_user = self.request.user
        return super(UploadPost, self).form_valid(form)


@login_required(login_url='/accounts/login/')
def delete_post(request, slug):
	if request.method == 'POST':
		post = Post.objects.get(slug=slug)
		post.delete()
	return redirect('/accounts/profile/')


@login_required(login_url='/accounts/login/')
def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_user = request.user
            comment.save()
            return redirect('post:postlist')
    else:
        form = CommentForm()
    return render(request, 'post/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post:postlist', pk=comment.post.pk)


@login_required(login_url='/accounts/login/')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post:postlist')
