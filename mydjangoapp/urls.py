from django.urls import path

from .views import *

urlpatterns = [
    path("forms/", FormListView.as_view(), name="form_list"),
    path("forms/create/", FormResponse.as_view(), name="form_create"),
    path("forms/<int:pk>/update/", FormUpdateView.as_view(), name="form_update"),
    path("forms/<int:pk>/delete/", FormDeleteView.as_view(), name="form_delete"),
    path("mcq/", McqResponse.as_view(), name="mcq_response"),
    path("mcqupdate/", McqResponseUpdate.as_view(), name="mcq_response_update"),
    ]