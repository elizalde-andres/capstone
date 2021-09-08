from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("test/<int:id>", views.test_view, name="test"),
    path("test/<int:id>/<int:assignment_id>", views.test_view, name="test"),
    path("teacher_results/<int:test_id>", views.teacher_results, name="teacher_results"),

    path("new_test/", views.new_test, name="new_test"),
    path("get_test/<int:id>", views.get_test, name="get_test"),
    path("edit_test/<int:id>", views.edit_test, name="edit_test"),
    path("answer/<int:assignment_id>", views.answer, name="answer"),
    path("update_score/<int:assignment_id>/<int:answer_id>", views.update_score, name="update_score"),
    path("assign/<int:id>", views.assign, name="assign"),
    path("unassign/<int:id>", views.unassign, name="unassign"),
    path("test_form_layout/<str:layout>", views.test_form_layout, name="test_form_layout")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)