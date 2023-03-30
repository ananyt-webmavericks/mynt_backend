
from django.urls import path

from .views import CompanyApiView, CompanyCreateApiView, GetCompanyByUserId

urlpatterns = [
    path('manage', CompanyApiView.as_view()),
    path('create', CompanyCreateApiView.as_view()),
    path('company-by-user-id/<int:id>', GetCompanyByUserId.as_view())
]