from django import forms

from .models import Category, Food


# class CategoryForm(forms.Form): customize all fields
class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "название категории",
                "class": "form-control",
            }
        )
    )
    max_age = forms.IntegerField(
        label="Максимальный возраст",
        initial=50,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "возраст"
            }
        )
    )
    foods = forms.ModelMultipleChoiceField(
        label="Корма",
        help_text="Выберите подходящие корма",
        widget=forms.CheckboxSelectMultiple,
        queryset=Food.objects.all().order_by('name'),
    )

    class Meta:
        model = Category
        # fields = "__all__"
        fields = ("name", "max_age", "foods", "img")
        # exclude = ("foods",)
