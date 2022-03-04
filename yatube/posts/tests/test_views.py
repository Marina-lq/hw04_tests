
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post
from posts.models import Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title='Заголовок группы',
            slug='group-slag',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse('post:index'): 'posts/index.html',
            reverse('post:group_posts', kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse('post:profile', kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('post:post_detail', kwargs={'post_id': self.post.pk}):
            'posts/post_detail.html',
            reverse('post:post_create'): 'posts/includes/post_create.html',
            reverse('post:edit', kwargs={'post_id': self.post.pk}):
            'posts/includes/post_create.html'
        }
        # Проверяем, что при обращении к name вызывается соответствующий
        # HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        # Проверка словаря контекста главной страницы (в нём передаётся форма)

    def test_page_show_correct_context(self):
        """Шаблоны сформирован с правильным контекстом."""
        templates_pages_names = [
            reverse('post:index'),
            reverse('post:group_posts', kwargs={'slug': self.group.slug}),
            reverse('post:profile', kwargs={'username':
                                            self.user.username})
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, self.post.text)
                self.assertEqual(first_object.author, self.post.author)
                self.assertEqual(first_object.group, self.post.group)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон task_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse('post:post_detail',
                                               kwargs={'post_id':
                                                       self.post.pk})))
        self.assertEqual(response.context.get('post').text, self.post.text)
        self.assertEqual(response.context.get('post').author, self.post.author)

    def test_create_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse('post:edit',
                                               kwargs={'post_id':
                                                       self.post.pk})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_show_correct_context(self):
        response = self.authorized_client.get(reverse('post:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_page_show_correct_post_with_group(self):
        """Шаблоны сформирован с правильным контекстом."""
        templates_pages_names = [
            reverse('post:index'),
            reverse('post:group_posts', kwargs={'slug': self.group.slug}),
            reverse('post:profile', kwargs={'username':
                                            self.user.username})
        ]
        for reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.group, self.post.group)
