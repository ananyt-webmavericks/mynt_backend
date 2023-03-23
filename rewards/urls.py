from django.urls import path

from .views import RewardsApiView

urlpatterns = [
    path('manage', RewardsApiView.as_view()),
]