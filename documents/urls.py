from django.urls import path

from .views import DocumentsApiView, GetDocumentsbyCompanyId,InitiateContractWithFounder,SignzyContractCallback

urlpatterns = [
    path('manage', DocumentsApiView.as_view()),
    path('get-documents-by-comapny-id/<int:id>', GetDocumentsbyCompanyId.as_view()),
    path('initiate-contract-with-founder', InitiateContractWithFounder.as_view()),
    path('signzy-callback', SignzyContractCallback.as_view()),

]