from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("upload/", views.upload_document, name="upload_document"),
    path("delete/<int:document_id>/", views.delete_document, name="delete_document"),
    path("edit/<int:document_id>/", views.edit_document, name="edit_document"),
    re_path(
        r"^media/documents/(?P<path>.*)$", views.view_document, name="view_document"
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("mainmenu/", views.main_menu, name="main_menu"),
    path("board_list/", views.board_list, name="board_list"),
    path("board/post/new/", views.post_create, name="post_create"),
    path("board/post/<int:post_id>/", views.post_detail, name="post_detail"),
]
