from rest_framework import serializers
from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Notes
        fields = ["title", "description", "created_by"]
        read_only_fields = ["creation_date", "modification_date"]
