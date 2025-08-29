from django.urls import path
from . import views

urlpatterns = [
    path('qr-generate/', views.QRCodeListCreateView.as_view()),
    path('qr-generate/<int:pk>/', views.QRCodeDetailView.as_view()),
]