from django.db import models

from client.models import NULLABLE


class Blogpost(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(**NULLABLE, verbose_name='содержимое')
    preview = models.ImageField(upload_to='blogposts/', **NULLABLE, verbose_name='изображение (превью)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
