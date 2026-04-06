from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("planner.urls")),
    path("pets/", include("pets.urls")),
    path("vaccines/", include("vaccines.urls")),
    path("common/", include("common.urls")),
]

# Custom error handlers
handler403 = "VetVax_Planner.views.custom_403"
handler404 = "VetVax_Planner.views.custom_404"
handler500 = "VetVax_Planner.views.custom_500"