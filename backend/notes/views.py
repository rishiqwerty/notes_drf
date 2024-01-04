from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotesSerializer
from rest_framework import status
from .models import Notes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q


# Create your views here.
class Note(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = NotesSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.validated_data['created_by'] = self.request.user
            serializer.save()
            return Response({"Status": "New Note Created!!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        note_id = kwargs.get('id')

        if note_id:
            print("here", note_id)
            try:
                note = Notes.objects.get(id=note_id, created_by=self.request.user.id)
                serializer = NotesSerializer(note)
            except Exception as e:
                print("Exception",e)
                return Response({'error': 'Note Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            con1 = Q(created_by=self.request.user.id)
            con2 = Q(alloted_user__contains=self.request.user.id)
            notes = Notes.objects.filter(con1 | con2)
            serializer = NotesSerializer(notes, many=True)
        return Response(serializer.data)
