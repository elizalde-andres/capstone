from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tests/", views.tests_view, name="tests"),
    path("test/<int:id>", views.test_view, name="test"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)