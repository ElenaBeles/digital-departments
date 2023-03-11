from django.urls import path

from web.views import main_view, auth_view, registration_view, article_edit_view, tags_view, tags_delete_view

urlpatterns = [
    path("", main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),

    path("article/add/", article_edit_view, name="article_add"),
    path("article/<int:id>/", article_edit_view, name="article_edit"),

    path("tags/", tags_view, name="tags"),
    path("tags/<int:id>/delete/", tags_delete_view, name="tags_delete"),
]
