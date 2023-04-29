from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор поста')

    group = models.ForeignKey(
        'Group', blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Выберите группу, к которой будет относиться пост')

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Загрузите картинку к посту',
    )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Введите название заголовка')
    slug = models.SlugField(
        'Адрес',
        max_length=200,
        unique=True,
        help_text='Укажите адрес группы')
    description = models.TextField(
        'Описание',
        help_text='Дайте описание группы')

    class Meta:
        verbose_name = 'группу'
        verbose_name_plural = 'Группы'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария')
    created = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} на пост {self.post}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_author')
        ]
        verbose_name = 'подписку'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'


class Preferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
