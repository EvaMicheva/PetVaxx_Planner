from django.urls import path
from . import views

app_name = "vaccines"

urlpatterns = [
    path("", views.vaccine_list, name="list"),
    path("<int:pk>/", views.VaccineDetailView.as_view(), name="detail"),
    path("api/list/", views.VaccineListAPI.as_view(), name="api_list"),
]
