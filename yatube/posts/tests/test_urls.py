# posts/tests/test_urls.py
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post
from posts.models import User

User = get_user_model()


class StaticURLTests(TestCase):
    def test_homepage(self):
        # Создаем экземпляр клиента
        guest_client = Client()
        # Делаем запрос к главной странице и проверяем статус
        response = guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_group_list(self):
        guest_client = Client()
        response = guest_client.get('/group/')
        self.assertEqual(response.status_code, 404)

    def test_profile(self):
        guest_client = Client()
        response = guest_client.get('/profile/')
        self.assertEqual(response.status_code, 404)

    def test_post_detail(self):
        guest_client = Client()
        response = guest_client.get('/posts/')
        self.assertEqual(response.status_code, 404)

    def test_unexisting_page(self):
        guest_client = Client()
        response = guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list(self):
        response = self.guest_client.get('/group/')
        self.assertEqual(response.status_code, 404)

    def test_post_detail(self):
        response = self.guest_client.get('/posts/')
        self.assertEqual(response.status_code, 404)

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
    # Проверяем доступность страниц для авторизованного пользователя

    def test_create_post(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_edit(self):
        response = self.authorized_client.get('/edit/')
        self.assertEqual(response.status_code, 404)
