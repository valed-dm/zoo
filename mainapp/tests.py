from django.test import TestCase

from .models import Category, Food


class TestFood(TestCase):

    # выполняется перед каждым тестом
    def setUp(self):
        self.food = Food.objects.create(name="Банан")
        print("TestFood: Я выполняюсь перед каждым тестом")

    # выполняется после каждого теста
    def tearDown(self) -> None:
        print("TestFood: Я выполняюсь после каждого теста")

    def test_init(self):
        self.assertEqual(self.food.name, "Банан")

    def test_str(self):
        self.assertEqual(str(self.food), "Банан")


class TestCategory(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Травоядные")
        print("TestCategory: Я выполняюсь перед каждым тестом")

    # выполняется после каждого теста
    def tearDown(self) -> None:
        print("TestCategory: Я выполняюсь после каждого теста")

    def test_count_category_foods(self):
        names = ["вода", "трава", "зерно", "овощи"]
        for name in names:
            food = Food.objects.create(name=name)
            self.category.foods.add(food)
        self.category.save()
        self.assertEqual(self.category.count_category_foods(), 4)

    def test_some_error(self):
        with self.assertRaises(ValueError):
            self.category.some_error()
