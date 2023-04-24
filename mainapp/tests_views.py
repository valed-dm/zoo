from django.test import TestCase

from userapp.models import MyUser
from .models import Animal, Category


class TestViews(TestCase):
    # 1. Страница отвечает
    # 2. На страницу передаются нужные данные
    # 3. На странице есть кнопка "Поиск"
    # 3. ? Данные выводятся на странице - под вопросом

    # писать на каждую страницу, показывает, что страница отвечает
    def test_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # есть плюсы и минусы - нам нужно знать, показывается ли страница,
    # а сам контекст неважен - решать самостоятельно, нужен ли такой тест или нет
    # нужно учитывать, что при изменении контекста тесты будут падать
    def test_context(self):
        # на страницу передаются данные о животных и категориях
        # нужно создать категорию и животного
        # сама категория для теста не нужна, но животное связано с ней в модели!
        category = Category.objects.create(name="Плотоядные")
        # Созданный объект animal не нужен (animal = Animal.objects.create(name="Борис", category=category))
        # т.к. сохраняется в БД и подтягивается из нее:
        # таки нужен:
        animal = Animal.objects.create(name="Борис", category=category)
        response = self.client.get("/")
        # print(response.context)
        self.assertEqual("animals" in response.context, True)
        self.assertTrue("animals" in response.context)
        self.assertEqual(response.context["animals"].first().id, animal.id)

    def test_content(self):
        response = self.client.get("/")
        # print("html content ===>", response.content)
        user_element = '<button class="btn btn-outline-success" type="submit">Поиск</button>'
        # response decoding
        self.assertIn(user_element, response.content.decode(encoding="utf-8"))
        # user element encoding
        self.assertIn(user_element.encode(encoding="utf-8"), response.content)

    # user authorization test
    def test_category_list_auth(self):
        # this request is sent by an unauthorized user
        response = self.client.get("/category-list/")
        self.assertEqual(response.status_code, 302)

        # first, we need a User object with create_user to get hashed user password
        user = MyUser.objects.create_user(
            username="auth_user",
            email="auth@user.com",
            password="admin12345"
        )
        # after this, our user is authorized at a django client side
        # and all requests are sent from his name
        self.client.login(username="auth_user", password="admin12345")
        # now we are waiting for response code 200 from user already authorized
        response = self.client.get("/category-list/")
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        response = self.client.get("/category-list/")
        self.assertEqual(response.status_code, 302)

    def test_category_create_auth(self):
        response = self.client.get("/category-create/")
        self.assertEqual(response.status_code, 302)

        user = MyUser.objects.create_user(
            username="auth_user",
            email="auth@user.com",
            password="admin12345"
        )

        self.client.login(username="auth_user", password="admin12345")

        # now we authorized as user, but permission must be denied
        # cause user has no rights to create a category:
        # res -> Forbidden (Permission denied): /category-create/
        response = self.client.get("/category-create/")
        self.assertEqual(response.status_code, 403)

        self.client.logout()

        # user is_staff=True
        user = MyUser.objects.create_user(
            username="staff_user",
            email="staff@user.com",
            password="admin12345",
            is_staff=True
        )

        # permission to create category is granted to this user
        self.client.login(username="staff_user", password="admin12345")

        response = self.client.get("/category-create/")
        # now the response code is 200
        self.assertEqual(response.status_code, 200)
