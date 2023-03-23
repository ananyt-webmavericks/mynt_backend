from django.urls import path

from .views import FaqsApiView

urlpatterns = [
    path('manage', FaqsApiView.as_view()),
]