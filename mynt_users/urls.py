
from django.urls import path

from mynt_users.views import MyntUsersApiView,EmailVerifyView,SendOTPOnMail,GetUserById,LoginUserByEmail, MyntUserCreateApiview
from .utils import UploadFiles
urlpatterns = [
    path('manage', MyntUsersApiView.as_view()),
    path('verify-email-otp', EmailVerifyView.as_view()),
    path('send-otp', SendOTPOnMail.as_view()),
    path('<int:id>', GetUserById.as_view()),
    path('login', LoginUserByEmail.as_view()),
    path('sign-up', MyntUserCreateApiview.as_view()),
    path('upload-files', UploadFiles.as_view()),
]