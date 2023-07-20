from django.urls import path
from kitchen.views import (
    Index, CookListView, CookCreateView,
    CookUpdateView, CookDetailView, IngredientListView,
    IngredientCreateView, IngredientUpdateView, DishTypeList,
    IngredientDeleteView, CookDeleteView, DishTypeCreateView,
    DishTypeDeleteView, DishTypeUpdateView, DishListView,
    DishCreateView
)

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/details", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/<int:pk>/delete", CookDeleteView.as_view(), name="cook-delete"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/create/", IngredientCreateView.as_view(), name="ingredient-create"),
    path("ingredients/<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient-update"),
    path("ingredients/<int:pk>/delete", IngredientDeleteView.as_view(), name="ingredient-delete"),
    path("dish-types/", DishTypeList.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dishes", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create")
]

app_name = "kitchen"
