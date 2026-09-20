from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet,UpdateList,save_results

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
    path('latest_quiz/', QuizViewSet.as_view({'get': 'latest_quiz'})),
    path('updates/', UpdateList.as_view(), name='update-list'),
    path('save_results/', save_results, name='save_results')
]
