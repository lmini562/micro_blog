from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import BlogListView, BlogDetailView, CreatePost, CreateUser, CustomLoginUser, add_like

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('create/post/', CreatePost.as_view(), name='create_post'),
    path('auth/', CustomLoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('like/', add_like, name='like'),
]
