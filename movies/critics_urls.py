from django.urls import path
from .views import CriticListView, CriticDetailView

urlpatterns = [
    path('', CriticListView.as_view(), name='critic_list'),
    path('<uuid:pk>/', CriticDetailView.as_view(), name='critic_detail'),
]