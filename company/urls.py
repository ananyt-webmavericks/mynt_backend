
from django.urls import path

from .views import CompanyApiView, CompanyCreateApiView, GetCompanyByUserId,GetCompanyCount

urlpatterns = [
    path('manage', CompanyApiView.as_view()),
    path('create', CompanyCreateApiView.as_view()),
    path('company-by-user-id/<int:id>', GetCompanyByUserId.as_view()),
    path('count', GetCompanyCount.as_view())
]