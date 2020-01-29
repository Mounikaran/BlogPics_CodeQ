from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

from account.forms import UserForm, ProfileEditForm
from post.models import Post
from codeq.models import Question

# Create your views here.


class SignUpView(generic.CreateView):
	form_class = UserForm
	model = User
	template_name = 'account/signup.html'
	success_url = reverse_lazy('account:login')


class ProfileView(LoginRequiredMixin, generic.ListView):
	model = Post
	template_name = 'account/profile.html'
	slug_field = 'username'

class CodeQProfile(LoginRequiredMixin, generic.ListView):
	model = Question
	template_name = 'account/codeq_profile.html'

class DeleteAccount(LoginRequiredMixin, generic.DeleteView):
	login_url = '/accounts/login/'
	model = User
	template_name = 'account/account_delete_confirm.html'
	context_object_name = 'object'
	success_url = reverse_lazy('account:signup')


@login_required(login_url='/accounts/login/')
def edit_profile(request):
	if request.method == 'POST':
		 form = ProfileEditForm(data=request.POST, instance=request.user)

		 if form.is_valid():
		 	form.save()
		 	return redirect('/accounts/profile/')
	else:
		form = ProfileEditForm(instance=request.user)

	return render(request, 'account/edit_profile.html', {'form':form})

@login_required(login_url='/accounts/login/')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('/accounts/profile/')
		else:
			return redirect('accounts/profile/change-password')

	else:
		form = PasswordChangeForm(user=request.user)

	return render(request, 'account/change_password.html', {'form':form})
