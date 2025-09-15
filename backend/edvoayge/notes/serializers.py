from rest_framework import serializers

from rest_framework import serializers
from .models import NotesCategory, NotesVideoMain, NotesVideoSub, NotesVideoPlayer


class NotesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesCategory
        fields = ['id', 'name']


class NotesVideoMainSerializer(serializers.ModelSerializer):
    category = NotesCategorySerializer(read_only=True)

    class Meta:
        model = NotesVideoMain
        fields = ['id', 'title', 'category']


class NotesVideoSubSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='title.title', read_only=True)  # only topic title

    class Meta:
        model = NotesVideoSub
        fields = ['id', 'title', 'doctor', 'duration', 'logo', 'free']


class NotesVideoPlayerSerializer(serializers.ModelSerializer):
    video = NotesVideoSubSerializer(read_only=True)

    class Meta:
        model = NotesVideoPlayer
        fields = ['id', 'video', 'completed']

