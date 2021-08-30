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
    path("new_test/", views.new_test, name="new_test"),
    path("edit_tests/", views.edit_tests, name="edit_tests"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)