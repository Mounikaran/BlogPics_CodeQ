from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from braces.views import FormValidMessageMixin
from django.views import generic
from django.http import HttpResponseRedirect

from codeq.models import Question, Answer, Reply
from codeq.forms import QuestionForm, AnswerForm, ReplyForm


# Create your views here

class QuestionList(generic.ListView):
    model = Question
    template_name = 'codeq/question_list.html'

class QuestionDetail(generic.DetailView):
    model = Question
    template_name = 'codeq/question_detail.html'
    context_object_name = 'question'

class DeleteQuestion(LoginRequiredMixin, FormValidMessageMixin, generic.DeleteView):
    template_name = 'codeq/delete_confirm.html'
    model = Question
    success_url = reverse_lazy('codeq:question_list')
    form_valid_message = 'Question Deleted Successfully'

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(slug=kwargs['slug'])

        if(question.question_user != request.user):
            return HttpResponseRedirect(reverse_lazy('codeq:question_detail', kwargs={'slug':kwargs['slug']}))
        else:
            return super(DeleteQuestion, self).get(request, *args, *kwargs)

class UploadQuestion(LoginRequiredMixin, generic.CreateView):
    form_class = QuestionForm
    model = Question
    template_name = 'codeq/question_form.html'
    success_url = reverse_lazy('codeq:question_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question_user = self.request.user
        return super(UploadQuestion, self).form_valid(form)


@login_required(login_url="/accounts/login/")
def add_answer(request, slug):
    question = get_object_or_404(Question, slug=slug)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.answered_user = request.user
            answer.save()
            return redirect('codeq:question_detail', slug=slug)
    else:
        form = AnswerForm()
    return render(request, 'codeq/answer_form.html', {'form':form})

@login_required(login_url='/accounts/login/')
def delete_answer(request, slug):
    answer = get_object_or_404(Answer, slug=slug)
    answer.delete()
    return redirect('codeq:question_list')

@login_required(login_url="/accounts/login/")
def add_reply(request, slug):
    answer = get_object_or_404(Answer, slug=slug)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.answer = answer
            reply.reply_user = request.user
            reply.save()
            return redirect('codeq:question_list')
    else:
        form = ReplyForm()
    return render(request, 'codeq/reply_form.html', {'form':form})

@login_required(login_url='/accounts/login/')
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('codeq:question_list')
