# blog1/views.py
# Add these views to your existing views.py file

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Profile
from .forms import ProfileUpdateForm
from django.http import HttpResponse
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if current user is following this profile
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user.profile.is_following(self.get_object())
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_edit.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'username': self.request.user.username})

class FollowersListView(ListView):
    model = Profile
    template_name = 'followers_list.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return profile.followers.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return context

class FollowingListView(ListView):
    model = Profile
    template_name = 'following_list.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return profile.following.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return context

@login_required
def follow_toggle(request, username):
    profile_to_toggle = get_object_or_404(Profile, user__username=username)
    user_profile = request.user.profile
    
    if user_profile.is_following(profile_to_toggle):
        user_profile.unfollow(profile_to_toggle)
        is_following = False
    else:
        user_profile.follow(profile_to_toggle)
        is_following = True
    
    return JsonResponse({
        'success': True,
        'is_following': is_following,
        'followers_count': profile_to_toggle.followers_count
    })
def home(request):
    return HttpResponse("Welcome to the homepage!")