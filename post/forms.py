from django import forms

from post.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'image', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Comment here'
