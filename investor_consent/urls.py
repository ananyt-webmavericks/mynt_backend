from django.urls import path

from investor_consent.views import InvestorConsentAPIView,GetConsentByUserId

urlpatterns = [
    path('manage', InvestorConsentAPIView.as_view()),
    path('<int:user_id>', GetConsentByUserId.as_view())
]