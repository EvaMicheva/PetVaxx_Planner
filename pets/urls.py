from django.urls import path
from .views import pet_list, PetDetailView, PetCreateView, PetUpdateView, PetDeleteView

app_name = "pets"

urlpatterns = [
    path("", pet_list, name="list"),
    path("add/", PetCreateView.as_view(), name="add"),
    path("<int:pk>/", PetDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PetUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", PetDeleteView.as_view(), name="delete"),
]
