from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotesSerializer, SharedNoteSerializer
from rest_framework import status
from .models import Notes, NoteShare
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Create your views here.
class Note(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.validated_data["created_by"] = self.request.user
            serializer.save()
            return Response({"status": "New Note Created!!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get("id")

        if note_id:
            try:
                note = Notes.objects.get(id=note_id, created_by=self.request.user.id)
                serializer = NotesSerializer(note)
            except Exception as e:
                print("Exception", e)
                try:
                    note = NoteShare.objects.get(note=note_id, sharing_status=True).note
                except:
                    return Response(
                        {"error": "Note Not Found"}, status=status.HTTP_404_NOT_FOUND
                    )
        else:
            # Check for Shared notes
            shared_notes = NoteShare.objects.filter(
                shared_with=self.request.user.id, sharing_status=True
            ).values("note")
            shared_notes_ids = [i.get("note") for i in shared_notes]
            con1 = Q(created_by=self.request.user.id)
            con2 = Q(id__in=shared_notes_ids)
            notes = Notes.objects.filter(con1 | con2).order_by("-modification_date")
            serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        note_id = kwargs.get("id")

        if note_id is not None:
            try:
                note = Notes.objects.get(id=note_id, created_by=self.request.user.id)
                print(note)
            except Notes.DoesNotExist:
                return Response(
                    {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = NotesSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "id not found"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get("id")
        if note_id is not None:
            try:
                note = Notes.objects.get(id=note_id)
                note.delete()
                return Response(
                    {"status": "Note Deleted!!"}, status=status.HTTP_404_NOT_FOUND
                )
            except Notes.DoesNotExist:
                return Response(
                    {"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "id not found"}, status=status.HTTP_400_BAD_REQUEST
            )

class NoteSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")

        if query:
            # Perform a case-insensitive search using trigram similarity
            search_vector = SearchVector("title", "description", config="english")
            search_query = SearchQuery(query, config="english")
            results = (
                Notes.objects.annotate(
                    similarity=SearchRank(search_vector, search_query)
                )
                .filter(
                    (Q(description__icontains=query) | Q(title__icontains=query)),
                    Q(created_by=request.user.id),
                )
                .order_by("-similarity")
            )

            serializer = NotesSerializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "No query provided"}, status=status.HTTP_400_BAD_REQUEST
            )


class NoteShareView(APIView):
    def post(self, request, note_id, *args, **kwargs):
        serializer = SharedNoteSerializer(
            data=request.data, context={"request": request, "note_id": note_id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
