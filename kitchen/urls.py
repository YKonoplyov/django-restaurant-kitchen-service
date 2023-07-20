from django.urls import path
from kitchen.views import Index, CookListView, CookCreateView, CookUpdateView, CookDetailView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/details", CookDetailView.as_view(), name="cook-detail")
]

app_name = "kitchen"
