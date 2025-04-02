from django.urls import path
from .views import MeterReadingCreateAPIView, UserBillListAPIView, UserBillDetailAPIView

urlpatterns = [
    path('readings/', MeterReadingCreateAPIView.as_view(), name='add-reading-api'),
    path('bills/', UserBillListAPIView.as_view(), name='user-bills-list-api'),
    path('bills/<int:pk>/', UserBillDetailAPIView.as_view(), name='user-bills-detail-api'),
]