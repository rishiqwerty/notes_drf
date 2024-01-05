import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from notes.models import NoteShare
from datetime import datetime

def deactivate_notes():
    '''
        This is for deactivating shared notes which were shared for certain duration of time 
    '''
    notes_shared = NoteShare.objects.filter(shared_duration__gt=datetime.now())
    if notes_shared:
        for i in notes_shared:
            i.sharing_status = False
            i.save()

if __name__=='__main__':
    deactivate_notes()