from rest_framework import serializers
from notes.models import Notes, NoteShare
from django.contrib.auth import get_user_model

User = get_user_model()


class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteShare
        fields = ["shared_with", "shared_duration", "sharing_status"]

    def create(self, validated_data):
        context = self.context.get("request")
        user_to_share_with_id = (
            context.data.get("shared_with", None) if context else None
        )
        if not user_to_share_with_id:
            raise serializers.ValidationError(
                {"detail": "Please provide the user to whom note to be shared"}
            )
        try:
            user_to_share_with = User.objects.get(id=user_to_share_with_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "Please provide the user to whom note to be shared"}
            )
        try:
            note_id = self.context.get("note_id")
            note = Notes.objects.get(id=note_id)
        except:
            raise serializers.ValidationError({"detail": "Note does not exist"})
        if NoteShare.objects.filter(
            note=note, sharing_status=True, shared_with=user_to_share_with_id
        ).exists():
            raise serializers.ValidationError(
                {"detail": "Note already shared with the user"}
            )
        if Notes.objects.filter(created_by=user_to_share_with_id):
            raise serializers.ValidationError(
                {"detail": "Note is created by this shared user itself"}
            )
        if user_to_share_with:
            note_share = NoteShare.objects.create(
                note=note,
                shared_with=user_to_share_with,
                shared_duration=context.data.get("shared_duration", None)
                if context
                else None,
                sharing_status=context.data.get(
                    "sharing_status", True if context else True
                ),
            )

            return note_share


class NotesSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Notes
        fields = ["title", "description", "created_by"]
        read_only_fields = ["creation_date", "modification_date"]


# {
#     "title":"Note9",
#     "description": "Note 9 is created"
# }
# { // Specify the duration in seconds (e.g., 1 hour)
#   "sharing_status": true,  // Specify the initial sharing status
#   "shared_with": 3  // The ID of the user to share the note with
# }
