from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
   
  path('videos/overview/', views.video_overview, name='video_overview'),
    path('videos/topics/', views.video_topic_breakdown, name='video_topic_breakdown'),
    path('videos/details/', views.video_details, name='video_details'),
    path('videos/urls/', views.video_urls, name='video_urls'),

    

] 