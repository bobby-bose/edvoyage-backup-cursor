from django.urls import path
from . import views
from .mcq import views as mcqviews
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
    # ================================================

    path('mcq/categories/', mcqviews.get_categories),
    path('mcq/topics/<int:category_id>/', mcqviews.get_topics_by_category),
    path('mcq/questions/<int:topic_id>/', mcqviews.get_questions_by_topic),
path('clinical-notes/', mcqviews.get_clinical_categories_with_notes, name='clinical-notes'),
] 