
from django.urls import path

from .views import CompanyApiView

urlpatterns = [
    path('manage', CompanyApiView.as_view())
]