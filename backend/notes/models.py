from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    alloted_user = models.JSONField(default=list)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    
class NoteShare(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='shared_notes')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_user')
    shared_duration = models.DateTimeField(default=None, null=True)
    sharing_status = models.BooleanField(null=False, blank=False, default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
