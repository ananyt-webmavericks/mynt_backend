from django.urls import path

from .views import CampaignApiView, CampaignByCompanyId, GetCmapaignById, GetAllCmapaignByStatus, GetCampaignWithCompanyDataByCampaignId

urlpatterns = [
    path('manage', CampaignApiView.as_view()),
    path('campaign-by-company-id/<int:id>', CampaignByCompanyId.as_view()),
    path('campaign-by-id/<int:id>', GetCmapaignById.as_view()),
    path('campaign-by-status', GetAllCmapaignByStatus.as_view()),
    path('campaign-with-company-data-by-campaign-id/<int:id>', GetCampaignWithCompanyDataByCampaignId.as_view()),
]