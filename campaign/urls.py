from django.urls import path

from .views import CampaignApiView, CampaignByCompanyId, GetCmapaignById, GetAllCmapaignByStatus, GetCampaignWithAllDataByCampaignId,GetCampaignsCount,GetCampaignForAdmin

urlpatterns = [
    path('manage', CampaignApiView.as_view()),
    path('campaign-by-company-id/<int:id>', CampaignByCompanyId.as_view()),
    path('campaign-by-id/<int:id>', GetCmapaignById.as_view()),
    path('campaign-by-status', GetAllCmapaignByStatus.as_view()),
    path('campaign-with-all-data-by-campaign-id/<int:id>', GetCampaignWithAllDataByCampaignId.as_view()),
    path('count', GetCampaignsCount.as_view()),
    path('manage/admin', GetCampaignForAdmin.as_view()),
]