from django.urls import path

from .views import CampaignApiView, CampaignByCompanyId

urlpatterns = [
    path('manage', CampaignApiView.as_view()),
    path('campaign-by-company-id/<int:id>', CampaignByCompanyId.as_view()),
]