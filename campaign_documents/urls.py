
from django.urls import path

from .views import CampaignDocument

urlpatterns = [
    path('campaign-agreement', CampaignDocument.as_view())
]