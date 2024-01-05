from django.urls import path
from .views import Note, NoteSearchView, NoteShareView

urlpatterns = [
    path("", Note.as_view(), name="notes"),
    path("<int:id>/", Note.as_view(), name="note-detail"),
    path("search/", NoteSearchView.as_view(), name="notes-search"),
    path("<int:note_id>/share/", NoteShareView.as_view(), name="note-share"),
]
