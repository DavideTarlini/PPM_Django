from django.urls import path
from .views import *

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing-page"),
    path("details/<int:pk>", CampaignDetailsView.as_view(), name="campaign-details"),
    path("sign up/", SignUpView.as_view(), name="sign-up"),
    path("login/", CustomLoginView.as_view(), name="login"),
]