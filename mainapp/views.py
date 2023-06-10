from typing import Any
from django.views.generic.list import ListView
from django.views.generic import DetailView
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
