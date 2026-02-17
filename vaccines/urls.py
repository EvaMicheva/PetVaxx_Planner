from django.urls import path
from .views import vaccine_list, VaccineDetailView

app_name = "vaccines"

urlpatterns = [
    path("", vaccine_list, name="list"),
    path("<int:pk>/", VaccineDetailView.as_view(), name="detail"),
]
