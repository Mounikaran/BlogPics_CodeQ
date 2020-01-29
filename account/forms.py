from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, label='First Name')
    last_name = forms.CharField(max_length=40, label='Last Name')
    email = forms.EmailField(max_length=40, required=True, label='Email')

    class Meta:
        model = User
        fields = ('username' ,'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'email',)
