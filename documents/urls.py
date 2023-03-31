from django.urls import path

from .views import DocumentsApiView, GetDocumentsbyCompanyId

urlpatterns = [
    path('manage', DocumentsApiView.as_view()),
    path('get-documents-by-comapny-id/<int:id>', GetDocumentsbyCompanyId.as_view()),

]