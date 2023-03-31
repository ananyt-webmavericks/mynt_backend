from django.urls import path

from .views import PressApiView, GetPressbyCompanyId

urlpatterns = [
    path('manage', PressApiView.as_view()),
    path('get-press-by-company-id/<int:id>', GetPressbyCompanyId.as_view()),
]