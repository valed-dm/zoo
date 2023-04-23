from django.core.management.base import BaseCommand

from mainapp.models import Animal, Category, Card, Food


class Command(BaseCommand):
    help = 'Fills in database'

    def handle(self, *args, **options):
        # ----------------------------------------------------------------------
        # field types
        # ----------------------------------------------------------------------
        # Time
        # models.DateField, models.DateTimeField, models.TimeField
        # Number
        # models.IntegerField, models.PositiveIntegerField, models.SmallIntegerField
        # Float
        #  models.FloatField, models.DecimalField
        # Bool
        # models.BooleanField
        # Blob, clob
        # models.ImageField, models.FileField, models.BinaryField
        # Enum -> chose from a list of values
        # models.CharField(max_length=32, choices=)
        #
        # models.UrlField
        # models.EmailField
        # ----------------------------------------------------------------------
        # create. read. update, delete
        # ----------------------------------------------------------------------
        # delete
        Animal.objects.all().delete()
        Category.objects.all().delete()
        Card.objects.all().delete()
        Food.objects.all().delete()
        # create
        category = Category.objects.create(name="Травоядное")
        print(category)
        print(type(category))
        print(category.name)
        # update
        category.name = "Птицы"
        category.save()
        print(category.name)
        # delete one
        category.delete()
        # ----------------------------------------------------------------------
        # Category
        # ----------------------------------------------------------------------
        herbivorous = Category.objects.create(name="Травоядные")
        predators = Category.objects.create(name="Хищники")
        birds = Category.objects.create(name="Птицы")
        # ----------------------------------------------------------------------
        # Food
        # ----------------------------------------------------------------------
        meat = Food.objects.create(name="Мясо")
        oatmeal = Food.objects.create(name="каша")
        hay = Food.objects.create(name="Сено")
        water = Food.objects.create(name="Вода")
        grain = Food.objects.create(name="Зерно")
        honey = Food.objects.create(name="Мед")
        # ----------------------------------------------------------------------
        # many-to-many
        # https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/
        # ----------------------------------------------------------------------
        herbivorous.foods.set([hay, water])
        predators.foods.set([meat, oatmeal, water])
        birds.foods.set([grain, water])

        # category is filled with objects, not strings
        bear = Animal.objects.create(name="Медведь", nickname="Василий", max_age=40, category=predators)
        bear_1 = Animal.objects.create(name="Медведь", nickname="Борис", max_age=40, category=predators)
        tiger = Animal.objects.create(name="Тигр Белый", nickname="Амур", max_age=50, category=predators)
        cow = Animal.objects.create(name="Корова", nickname="Василиса", max_age=30, category=herbivorous)
        bird = Animal.objects.create(name="Попугай", nickname="Попка", max_age=150, category=birds)

        bear.category.foods.add(honey)

        # ----------------------------------------------------------------------
        # select queries
        # ----------------------------------------------------------------------
        # select all data ->  <QuerySet [<Category: Травоядные>, <Category: Хищники>, <Category: Птицы>]>
        print("all data from categories ===>", Category.objects.all())
        print("all data from foods ===>", Food.objects.all())
        print("all data from animals ===>", Animal.objects.all())
        # select one object (2 way: first or get() sqlalchemy - 3 ways)
        # first
        print("1 from categories ===>", Category.objects.all().first())
        print("1 from foods ===>", Food.objects.all().first())
        print("1 from animals ===>", Animal.objects.all().first())
        # get()
        print("get(id) from animals ===>", Animal.objects.all().get(id=bear.id))
        print("get(id) from animals ===>", Animal.objects.all().get(id=bear_1.id).id)
        print("get(id) from animals ===>", Animal.objects.all().get(id=tiger.id))
        print("get(id) from animals ===>", Animal.objects.all().get(id=cow.id))
        print("get(id) from animals ===>", Animal.objects.all().get(id=bird.id))
        # filter()
        bears = Animal.objects.filter(name="Медведь")
        tigers = Animal.objects.filter(name="Тигр Белый")
        bear = Animal.objects.filter(name="Медведь", nickname="Василий")
        bear_1 = Animal.objects.filter(nickname="Борис")
        print("bears ===>", bears)
        print("tigers ===>", tigers)
        print("bear ===>", bear)
        print("bear_1 ===>", bear_1)
        # get all data where category != "Хищники"
        # Django: impossible to pass condition as arg!
        not_predators = Category.objects.exclude(name="Хищники")
        print("not_predators ===>", not_predators)
        for i in not_predators:
            print(i.__dict__['id'], i.__dict__['name'], end=": foods = ")
            print(i.foods.all())
            # 182 Травоядные: foods = <QuerySet [<Food: Сено>, <Food: Вода>]>
            # 184 Птицы: foods = <QuerySet [<Food: Вода>, <Food: Зерно>]>
        # all animals who live greater than 30
        # field lookups from https://docs.djangoproject.com/en/4.1/ref/models/querysets/
        greater_than_30 = Animal.objects.filter(max_age__gt=100)
        print("greater_than__30 ===>", greater_than_30)
        # animal name contains "ведь"
        # field lookups from https://docs.djangoproject.com/en/4.1/ref/models/querysets/
        bears = Animal.objects.filter(name__contains="ведь")
        print("animal name contains 'ведь' ===>", bears)
        # animals with category name="Хищники"
        # use relation between tables: table Category -> field "name"
        animals = Animal.objects.filter(category__name="Хищники")
        print("animals with category name='Хищники'", animals)
        # animals with category name starts with "T"
        # use relation between tables: table Category -> field "name" and lookup startswith
        animals = Animal.objects.filter(category__name__startswith="Т")
        print("animals with category name starts with 'T'", animals)
        # many-to-many
        # who does drink water or eat hay?
        categories = Category.objects.filter(foods__in=[hay, water]).filter()
        print("who does drink water or eat hay?", categories)
        categories = Category.objects.filter(foods__name__in=["Сено", "Вода"]).filter(foods__name="Сено")
        print("who does drink water and eat hay?", set(categories))
