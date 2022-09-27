
from django.contrib import admin
from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/auth', views.index, name='index'),
    path("register", views.register, name='register'),
    path("home", views.home, name="home_page"),



    path("admin-panel", views.adminPanel, name="admin")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
