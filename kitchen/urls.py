from django.urls import path
from kitchen.views import Index, CookListView, CookCreateView, CookUpdateView, CookDetailView, IngredientListView, \
    IngredientCreateView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/details", CookDetailView.as_view(), name="cook-detail"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredints/create/", IngredientCreateView.as_view(), name="ingredient-create")
]

app_name = "kitchen"
