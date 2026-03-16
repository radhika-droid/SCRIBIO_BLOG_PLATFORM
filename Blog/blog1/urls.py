from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('profile/<str:username>/following/', views.FollowingListView.as_view(), name='following-list'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow-toggle'),

    # ✅ Add this to fix the 404
    path('api/follow/<str:username>/', views.follow_toggle, name='follow-toggle-api'),
]
