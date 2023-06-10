from django.urls import path
from .views import *

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing-page"),
    path("details/<int:pk>", CampaignDetailsView.as_view(), name="campaign-details"),
]