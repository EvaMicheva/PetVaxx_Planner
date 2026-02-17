from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.home, name="home"),
    path("plans/", views.PlanListView.as_view(), name="list"),
    path("plans/add/", views.PlanCreateView.as_view(), name="add"),
    path("plans/quick-add/", views.quick_plan_create, name="quick_add"),
    path("plans/<int:pk>/", views.PlanDetailView.as_view(), name="detail"),
    path("plans/<int:pk>/edit/", views.PlanUpdateView.as_view(), name="update"),
    path("plans/<int:pk>/delete/", views.PlanDeleteView.as_view(), name="delete"),
]