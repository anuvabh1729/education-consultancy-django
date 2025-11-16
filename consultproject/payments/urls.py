from django.urls import path
from .views import (
    CreatePayPalOrderView,
    CapturePayPalOrderView,
    ListStudentPaymentsView
)

urlpatterns = [
    path("create-order/", CreatePayPalOrderView.as_view()),
    path("capture/", CapturePayPalOrderView.as_view()),
    path("my-payments/", ListStudentPaymentsView.as_view()),
]
