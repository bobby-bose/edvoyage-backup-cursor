from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count

from .models import (
    NotesCategory, NotesVideoMain,NotesVideoPlayer,NotesVideoSub
)
admin.site.register(NotesCategory)
admin.site.register(NotesVideoMain)
admin.site.register(NotesVideoPlayer)
admin.site.register(NotesVideoSub)
