from django.urls import path

from .views import DealTermsApiView

urlpatterns = [
    path('manage', DealTermsApiView.as_view()),
]