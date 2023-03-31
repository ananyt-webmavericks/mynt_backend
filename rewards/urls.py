from django.urls import path

from .views import RewardsApiView, GetRewardsbyCampaignId

urlpatterns = [
    path('manage', RewardsApiView.as_view()),
    path('get-rewards-by-campaign-id/<int:id>', GetRewardsbyCampaignId.as_view()),
]