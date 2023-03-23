from django.urls import path

from .views import HighlightsApiView

urlpatterns = [
    path('manage', HighlightsApiView.as_view()),
]