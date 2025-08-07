from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet, QuizCategoryViewSet, QuestionViewSet, OptionViewSet,
    QuizAttemptViewSet, QuizAnalyticsViewSet, QuizShareViewSet, QuizTimerViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'categories', QuizCategoryViewSet, basename='quiz-category')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'options', OptionViewSet, basename='option')
router.register(r'attempts', QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'analytics', QuizAnalyticsViewSet, basename='quiz-analytics')
router.register(r'shares', QuizShareViewSet, basename='quiz-share')
router.register(r'timers', QuizTimerViewSet, basename='quiz-timer')

# URL patterns for quizzes app
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Quiz custom action URLs
    path('quizzes/<int:pk>/start/', QuizViewSet.as_view({'post': 'start_quiz'}), name='quiz-start'),
    path('quizzes/<int:pk>/submit/', QuizViewSet.as_view({'post': 'submit_quiz'}), name='quiz-submit'),
    path('quizzes/<int:pk>/results/', QuizViewSet.as_view({'get': 'results'}), name='quiz-results'),
    path('quizzes/<int:pk>/leaderboard/', QuizViewSet.as_view({'get': 'leaderboard'}), name='quiz-leaderboard'),
    path('quizzes/<int:pk>/share/', QuizViewSet.as_view({'post': 'share'}), name='quiz-share'),
    
    # Quiz list action URLs
    path('quizzes/search/', QuizViewSet.as_view({'get': 'search'}), name='quiz-search'),
    path('quizzes/statistics/', QuizViewSet.as_view({'get': 'statistics'}), name='quiz-statistics'),
    path('quizzes/featured/', QuizViewSet.as_view({'get': 'featured'}), name='quiz-featured'),
    path('quizzes/recent/', QuizViewSet.as_view({'get': 'recent'}), name='quiz-recent'),
    path('quizzes/popular/', QuizViewSet.as_view({'get': 'popular'}), name='quiz-popular'),
    path('quizzes/bulk-action/', QuizViewSet.as_view({'post': 'bulk_action'}), name='quiz-bulk-action'),
    
    # Category action URLs
    path('categories/<int:pk>/quizzes/', QuizCategoryViewSet.as_view({'get': 'quizzes'}), name='category-quizzes'),
    path('categories/<int:pk>/statistics/', QuizCategoryViewSet.as_view({'get': 'statistics'}), name='category-statistics'),
    path('categories/reorder/', QuizCategoryViewSet.as_view({'post': 'reorder'}), name='reorder-categories'),
    
    # Attempt action URLs
    path('attempts/<uuid:pk>/results/', QuizAttemptViewSet.as_view({'get': 'results'}), name='attempt-results'),
    
    # Timer action URLs
    path('timers/<int:pk>/pause/', QuizTimerViewSet.as_view({'post': 'pause'}), name='timer-pause'),
    path('timers/<int:pk>/resume/', QuizTimerViewSet.as_view({'post': 'resume'}), name='timer-resume'),
] 