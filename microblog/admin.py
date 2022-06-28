from django.contrib import admin
from .models import Post, Like, Comment

# Здесь регистрируются модели новые для админки
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
