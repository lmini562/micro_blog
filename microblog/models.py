from django.db import models


class Post(models.Model):
    """
    Модель поста
    """
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # авторы будут браться из стандартной джанговской модели юзеров
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    text = models.TextField()

    def __str__(self):
        return self.title


class Like(models.Model):
    """
    Модель для лайков
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Comment(models.Model):
    """
    Модель с комментариями
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    class Meta:
        ordering = ['-date']
