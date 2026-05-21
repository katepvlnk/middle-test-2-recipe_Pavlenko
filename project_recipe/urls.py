from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('recipe/', include('recipe.urls')),
    path('admin/', admin.site.urls),
]