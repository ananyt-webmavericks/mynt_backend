from django.urls import path

from .views import PressApiView

urlpatterns = [
    path('manage', PressApiView.as_view()),
]