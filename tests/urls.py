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
    path("assign/<int:id>", views.assign, name="assign"),
    path("unassign/<int:id>", views.unassign, name="unassign"),
    path("new_test/", views.new_test, name="new_test"),
    path("abm_test_layout/", views.abm_test_layout, name="abm_test_layout"),
    path("abm_testpart_layout/", views.abm_testpart_layout, name="abm_testpart_layout"),
    path("abm_question_layout/", views.abm_question_layout, name="abm_question_layout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)