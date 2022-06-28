"""
В данном модуле хранятся кастомные формы приложения
"""
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.forms.models import ModelForm

from microblog.models import Comment, Post

class LoginForm(AuthenticationForm):
    """
    Кастомное представление формы аутентификации
    """
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'username',
                'class': "form-control",
                'id': "UserInput",
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'password',
                'class': "form-control",
                'id': "PasswordInput",
            }
        )
    )


class PostForm(ModelForm):
    """
    Форма для создания поста
    """
    class Meta:
        model = Post
        exclude = ("date", )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control content"}),
            "author": forms.HiddenInput(),
        }


class CommentForm(ModelForm):
    """
    Форма для создания комментария
    """
    class Meta:
        model = Comment
        exclude = ("date", )
        fields = ('author', 'text', 'post',)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "post": forms.HiddenInput(),
            "author": forms.HiddenInput(),
        }
