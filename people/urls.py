from django.urls import path

from .views import PeopleApiView, GetPeoplesbyCompanyId

urlpatterns = [
    path('manage', PeopleApiView.as_view()),
    path('get-peoples-by-company-id/<int:id>', GetPeoplesbyCompanyId.as_view()),
]