from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from mainapp.models import Campaign, Reward, Comment

class LandingPageView(ListView):
    template_name = "landing_page.html"
    model = Campaign
    paginate_by = 20
    

class CampaignDetailsView(DetailView):
    template_name = "campaign_detail.html"
    model = Campaign

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["rewards"] = Reward.objects.filter(campaign=pk)
        context["comments"] = Comment.objects.filter(campaign=pk)
        return context


class SignUpView(CreateView):
    template_name = "auth_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    template_name = "auth_form.html"
    success_url = reverse_lazy("landing-page") #scoprire perchè non porta qui, altrimenti
                                               # ridirezionare all'url di profile