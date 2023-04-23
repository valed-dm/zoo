import random
from math import sqrt

from django.test import TestCase


# для проверки работы функции нужно заменить randint(1, 4) на предсказуемое значение
def add_to_random(value):
    return random.randint(1, 4) + value


def mock_randint(start, end, *args, **kwargs):
    return 3


class TestMath(TestCase):

    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3)

    def test_add_to_random(self):
        # заменяем функцию random.randint на контролируемую функцию mock_randint:
        random.randint = mock_randint
        result = add_to_random(10)
        self.assertEqual(result, 13)
