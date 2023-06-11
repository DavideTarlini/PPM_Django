from django.urls import path
from .views import *
from django.contrib.auth import views as auth

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing-page"),
    path("filtered/<int:pk>", LandingPageFilteredView.as_view(), name="landing-page-filtered"),
    path("details/<int:pk>", CampaignDetailsView.as_view(), name="campaign-details"),
    path("add comment:<int:camp_pk>", AddCommentView.as_view(), name="add-comment"),
    path("contribute:<int:camp_pk>", ContributeView.as_view(), name="contribute"),
    path("create/", CreateCampaignView.as_view(), name="create-campaign"),
    path("sign up/", SignUpView.as_view(), name="sign-up"),
    path("login/", auth.LoginView.as_view(template_name ='post_form.html'), name="login"),
    path('logout/', auth.LogoutView.as_view(next_page ='landing-page'), name ='logout'),
    path("accounts/profile/", AccountView.as_view(), name="profile"),
]