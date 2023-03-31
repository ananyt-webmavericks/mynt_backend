from django.urls import path

from .views import FaqsApiView, GetFaqsbyCampaignId

urlpatterns = [
    path('manage', FaqsApiView.as_view()),
    path('get-faqs-by-campaign-id/<int:id>', GetFaqsbyCampaignId.as_view()),
]