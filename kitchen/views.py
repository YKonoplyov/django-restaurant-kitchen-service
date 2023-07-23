from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import (
    CookForm, CookUpdateForm, IngredientForm,
    CookUsernameSearchForm, IngredientSearchForm, DishSearchForm,
    DishTypeSearchForm, DishForm
)
from kitchen.models import Cook, Ingredient, DishType, Dish


class Index(generic.View):

    def get_context_data(self, **kwargs):
        context = {
            "cooks": len(get_user_model().objects.all()),
            "dishes": len(Dish.objects.all()),
            "ingredients": len(Ingredient.objects.all()),
            "dish_types": len(DishType.objects.all())
        }
        return context

    def get(self, request):
        return render(
            request, "kitchen/index.html", context=self.get_context_data()
        )


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data()

        username = self.request.GET.get("username", "")

        context["search_field"] = CookUsernameSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        self.queryset = Cook.objects.all()
        form = CookUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data()

        name = self.request.GET.get("name", "")

        context["search_field"] = IngredientSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        self.queryset = Ingredient.objects.all()

        form = IngredientSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    form_class = IngredientForm
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    form_class = IngredientForm
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data()

        name = self.request.GET.get("name", "")

        context["search_field"] = DishSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        self.queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data()

        name = self.request.GET.get("name", "")

        context["search_field"] = DishSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        self.queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def get_success_url(self):

        success_url = reverse_lazy(
            "kitchen:dish-details", args=[self.object.pk]
        )

        return success_url


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


def cook_done_work(request, dish_id):
    cook = Cook.objects.get(id=request.user.id)
    dish = Dish.objects.get(id=dish_id)
    dish.finished_cooks.add(cook)
    dish.save()
    return redirect(
        reverse_lazy(
            'kitchen:dish-details', kwargs={"pk": dish_id}
        )
    )
