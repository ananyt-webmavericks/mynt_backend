
from django.urls import path

from .views import CompanyApiView, CompanyCreateApiView

urlpatterns = [
    path('manage', CompanyApiView.as_view()),
    path('create', CompanyCreateApiView.as_view())
]