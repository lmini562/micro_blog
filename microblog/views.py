import json
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.urls.base import reverse

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from .forms import CommentForm, LoginForm, PostForm
from .models import Like, Post



class BlogListView(ListView):
    """
    Отображение всех постов
    """
    queryset = Post.objects.order_by('-date').all()
    template_name = 'home.html'

ВВ
class BlogDetailView(FormMixin, DetailView): # новое
    """
    Детальное отображение отдельного поста
    """
    model = Post
    template_name = 'post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = self.request.user
        request.POST._mutable = False
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(BlogDetailView, self).form_valid(form)


class CustomLoginUser(LoginView):
    """
    Представление для отображения формы для авторизации
    """
    template_name = 'login.html'
    form_class = LoginForm


class CreateUser(CreateView):
    """
    Вьюшка для создания пользователя
    """
    success_url = reverse_lazy("home")

    form_class = UserCreationForm

    queryset = User.objects.all()

    template_name = "registration.html"


class CreatePost(LoginRequiredMixin, CreateView):
    """
    Вьюшка для создания поста
    """
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    queryset = Post.objects.all()
    form_class = PostForm

    template_name = "post_form.html"

    def post(self, request, *args, **kwargs):
        """
        Функция подменяет значение user на значение author
        """
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST._mutable = False

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required(login_url="login")
@require_POST
def add_like(request):
    """
    Функция добавляет лайк если произведен вход в систему
    """
    content_id = request.POST.get("post_id", None)
    user = request.user
    post = get_object_or_404(Post, pk=content_id)
    total_likes = 0
    if post.likes.filter(author=user).exists():
        post.likes.filter(author=user).delete()
    else:
        like = Like(author=user, post=post)
        like.save()
    total_likes = post.likes.count()
    ctx = {'likes_count': total_likes, 'message': "Ok"}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
