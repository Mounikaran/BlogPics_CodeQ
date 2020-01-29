from django import forms

from codeq.models import Question, Answer, Reply

class QuestionForm(forms.ModelForm):
    class Meta():
        model = Question
        fields = ('question', 'code', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].label = "What's the Question"
        self.fields['code'].label = "Code"


class AnswerForm(forms.ModelForm):
    class Meta():
        model = Answer
        fields = ('answer',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = "Your Answer"

class ReplyForm(forms.ModelForm):
    class Meta():
        model = Reply
        fields = ('reply',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reply'].label = "Reply"
