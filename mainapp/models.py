from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=32, unique=True)

    # categories = models.ManyToManyField(Category)

    def __str__(self):
        # return self.name + "thing"
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    max_age = models.IntegerField(default=0)
    foods = models.ManyToManyField(Food)
    img = models.ImageField(upload_to="category", blank=True, null=True)

    def count_category_foods(self):
        return self.foods.count()

    def some_error(self):
        raise ValueError("some error")

    def __str__(self):
        return self.name


# 1-*
class Animal(models.Model):
    name = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32, default="waiting to be nicknamed")
    max_age = models.PositiveIntegerField(default=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "|" + self.nickname


# 1-1
class Card(models.Model):
    text = models.TextField(blank=True, null=True)
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return self.animal.name
