from django.urls import path

from .views import CampaignApiView, CampaignByCompanyId, GetCmapaignById, GetAllCmapaignbyStatus

urlpatterns = [
    path('manage', CampaignApiView.as_view()),
    path('campaign-by-company-id/<int:id>', CampaignByCompanyId.as_view()),
    path('campaign-by-id/<int:id>', GetCmapaignById.as_view()),
    path('campaign-by-status', GetAllCmapaignbyStatus.as_view()),
]