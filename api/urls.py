from django.urls import path
from .views import QuestionAPIView

urlpatterns = [
    path('', QuestionAPIView.as_view()),
]
