from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CategoryForm
from .models import Animal, Category
from .tasks import get_metrics, send_email_task


# задача по правам и доступу:
# просмотр категорий доступен только авторизованным пользователям
# имя пользователя начинается на "u"
# категории удаляет только админ, а добавлять может сотрудник зоопарка
# остальные действия доступны всем

# Create your views here.
def index_view(request):
    # ForeignKey ---> select_related
    # many-to-many ---> prefetch_related
    res = get_metrics.delay(url=request.path, method=request.method)
    print("task ===>", res)
    print("task_id ===>", res.id)
    print("task_type ===>", type(res))
    print("task_status ===>", res.status)
    print("task_result ===>", res.result)

    # how to use in function logic authorization data
    # if request.user.is_superuser:

    animals = Animal.objects.all().select_related("category").prefetch_related("category__foods")
    return render(request, "mainapp/index_view.html", {"animals": animals})


@login_required
def contact_view(request):
    if request.method == "POST":
        text = request.POST.get("text")
        send_email_task.delay(
            from_email="dmvaled@gmail.com",
            to_email="valed_dm@mail.ru",
            title="test_django_mail",
            text=text
        )
        return render(request, "mainapp/contact_view.html")

    return render(request, "mainapp/contact_view.html")


# @user_passes_test(lambda user: user.is_superuser)
@user_passes_test(lambda user: user.username.startswith("u"))
def get_task_result_view(request, task_id):
    result = get_metrics.AsyncResult(task_id)

    context = {
        "task_id": result.id,
        "status": result.status,
        "result": result.result
    }
    return render(request, "mainapp/task_result.html", context=context)


# CRUD: CREATE, RETRIEVE, UPDATE, DELETE
# 5 pages
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    # template_name =
    # context_object_name =

    def get(self, request, *args, **kwargs):
        # print("get method CategoryListView ===>", request)
        return super().get(self, *args, *kwargs)

    def get_queryset(self):
        # default method
        return Category.objects.all()

    #     # modified method
    #     # return Category.objects.filter(is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["promo"] = " Рекламное сообщение"

        return context


class CategoryDetailView(DetailView):
    model = Category

    # def get(self, request, *args, **kwargs):
    #     pass
    #
    # # it's possible to filter returned objects by params here
    # # return Category.objects.filter(is_active=True)
    # def get_queryset(self):
    #     pass
    #
    # def get_object(self, queryset=None):
    #     pass
    #
    # def get_context_data(self, **kwargs):
    #     pass


class CategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    # fields = "__all__"
    form_class = CategoryForm
    success_url = "/category-list/"

    # func name = test_func!
    def test_func(self):
        # return self.request.user.email.endswith("@gmail.com")
        return self.request.user.is_staff

    # def get_form_kwargs(self):
    #     pass
    #
    # def get(self, request, *args, **kwargs):
    #     pass
    #
    # def get_context_data(self, **kwargs):
    #     pass
    #
    # def post(self, request, *args, **kwargs):
    #     pass
    #
    # def form_valid(self, form):
    #     pass
    #
    # def form_invalid(self, form):
    #     pass
    #
    # # redirect url assignment
    # def get_success_url(self):
    #     pass


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Category
    fields = "__all__"
    success_url = "/category-list/"

    # права через группы
    # например, врачи обновляют инфо о состоянии
    permission_required = "mainapp.change_category"


class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    model = Category
    success_url = "/category-list/"

    def test_func(self):
        return self.request.user.is_superuser
