from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('categories/', views.categories_view, name='categories'),
    path('topics/<int:topic_id>/video-lectures/', views.video_lectures_view, name='video_lectures'),
    path('categories/<str:category_name>/topics/', views.topics_view, name='topics'),
    path('topics/<int:topic_id>/modules/', views.modules_view, name='modules'),
    path('modules/track-view/', views.track_view, name='track_view'),
    path('mcq/track-attempt/', views.track_mcq_attempt, name='track_mcq_attempt'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('featured-content/', views.featured_content_view, name='featured_content'),


    path('notesvideos/',views.VideoLectureListView.as_view(), name='notes_videos'),

] 