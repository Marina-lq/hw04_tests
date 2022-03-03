# users/views.py
# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ContactForm
from django.shortcuts import redirect, render


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('post:profile')
    template_name = 'users/signup.html'


def only_user_view(request):
    if not request.user.is_authenticated:
        # Если пользователь не авторизован - отправляем его на страницу логина.
        return redirect('/auth/login/')
    # Если пользователь авторизован — здесь выполняется полезный код функции.


# views.py
def user_contact(request):
    ...
    # Создаём объект формы
    form = ContactForm()

    # И в словаре контекста передаём эту форму в HTML-шаблон
    return render(request, 'users/contact.html', {'form': form})
