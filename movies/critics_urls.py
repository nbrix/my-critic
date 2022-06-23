from django.urls import path
from .views import CriticListView, CriticDetailView, TopCriticsView

urlpatterns = [
    path('', CriticListView.as_view(), name='critic_list'),
    path('<uuid:pk>/', CriticDetailView.as_view(), name='critic_detail'),
    path('top', TopCriticsView.as_view(), name='top_critics'),
]