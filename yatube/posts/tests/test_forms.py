from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post
from posts.models import Group

User = get_user_model()


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.group_old = Group.objects.create(
            title='test_group_old',
            slug='test-slug-old',
        )
        cls.group_new = Group.objects.create(
            title='test_group_new',
            slug='test-slug-new',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group_old,
            text='Тестовый текст',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.guest_client = Client()

    def test_create_post(self):
        """Проверка формы создания нового поста."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group_old.id,
        }
        response = self.authorized_client.post(
            reverse('post:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('post:profile',
                                               kwargs={'username':
                                                       self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                group=self.group_old.id,
                text='Тестовый текст',
            ).exists()
        )

    def test_edit_post(self):
        """Проверка формы редактирования поста и изменение
        его в базе данных."""
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group_new.id,
        }
        response = self.authorized_client.post(
            reverse(
                'post:edit',
                kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'post:post_detail',
                kwargs={
                    'post_id': self.post.pk,
                }
            )
        )
        self.assertTrue(
            Post.objects.filter(
                group=self.group_new.id,
                text='Тестовый текст',
            ).exists()
        )
        self.assertFalse(
            Post.objects.filter(
                group=self.group_old.id,
                text='Тестовый текст',
            ).exists()
        )

    def test_guest_create_post(self):
        """Проверка формы создания нового поста."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group_old.id,
        }
        response = self.guest_client.post(
            ('post:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                group=self.group_old.id,
                text='Тестовый текст',
            ).exists()
        )
