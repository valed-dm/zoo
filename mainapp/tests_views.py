from django.test import TestCase

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
