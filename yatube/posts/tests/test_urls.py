from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestName')
        cls.user_not_author = User.objects.create_user(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_not_author = Client()
        self.authorized_client_not_author.force_login(self.user)
        cache.clear()

    def test_urls_client(self):
        test_pages = (
            ('/', self.guest_client, HTTPStatus.OK),
            (f'/group/{self.group.slug}/', self.guest_client, HTTPStatus.OK),
            (f'/profile/{self.post.id}/', self.guest_client,
             HTTPStatus.NOT_FOUND),
            (f'/posts/{self.post.id}/', self.guest_client, HTTPStatus.OK),
            ('/create/', self.authorized_client, HTTPStatus.OK),
            (f'/posts/{self.post.id}/edit/', self.authorized_client,
             HTTPStatus.OK),
        )
        for url, client, status in test_pages:
            with self.subTest(url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = (
            ('/', 'posts/index.html'),
            (f'/group/{self.group.slug}/', 'posts/group_list.html'),
            (f'/profile/{self.user.username}/', 'posts/profile.html'),
            (f'/posts/{self.post.id}/', 'posts/post_detail.html'),
            ('/create/', 'posts/post_create.html'),
            (f'/posts/{self.post.id}/edit/', 'posts/post_create.html'),
        )
        for url, template in templates_url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
