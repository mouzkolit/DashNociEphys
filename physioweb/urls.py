from django.urls import path

from physioweb.views import DashBoardView, HomeView, mRNAView, EphysDash

urlpatterns = [
    path('',  HomeView.as_view(), name='index'),
    path('dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('dashboard/mRNA', mRNAView.as_view(), name='mRNA'),
    path('ephys/', EphysDash.as_view(), name ='ephys' )
]