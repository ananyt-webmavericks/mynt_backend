from django.urls import path

from .views import CampaignApiView

urlpatterns = [
    path('manage', CampaignApiView.as_view()),
]