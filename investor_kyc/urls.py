
from django.urls import path

from investor_kyc.views import InvestorKycPanApiView,GetInvestorKyc,InvestorKycMobileApiView,SendMobileOtp,VerifyMobileOtp,InvestorKycAddressApiView,InvestorKycBankVerificationApiView,InvestorKycAadharApiView, GetAllInvestorKycDetails, UpdateInvestorKycApiView

urlpatterns = [
    path('pan/manage', InvestorKycPanApiView.as_view()),
    path('<int:user_id>', GetInvestorKyc.as_view()),
    path('mobile/manage', InvestorKycMobileApiView.as_view()),
    path('mobile/send-otp', SendMobileOtp.as_view()),
    path('mobile/verify-otp', VerifyMobileOtp.as_view()),
    path('address/manage', InvestorKycAddressApiView.as_view()),
    path('bank-verification/manage', InvestorKycBankVerificationApiView.as_view()),
    path('aadhaar-verification/manage', InvestorKycAadharApiView.as_view()),
    path('get-all-details-investor-Kyc', GetAllInvestorKycDetails.as_view()),
    path('update-investor-Kyc', UpdateInvestorKycApiView.as_view())
]