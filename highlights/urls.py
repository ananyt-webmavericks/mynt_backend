from django.urls import path

from .views import HighlightsApiView, GetHighlightsbyCampaignId

urlpatterns = [
    path('manage', HighlightsApiView.as_view()),
    path('get-highlights-by-campaign-id/<int:id>', GetHighlightsbyCampaignId.as_view()),
]