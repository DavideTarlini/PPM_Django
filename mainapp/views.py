from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
from mainapp.forms import CampaignCreationForm, CommentCreationForm, ContributionForm
from mainapp.models import Campaign, Reward, Comment, Contribution, CampaignCategory

class LandingPageView(ListView):
    template_name = "landing_page.html"
    model = Campaign

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CampaignCategory.objects.all() 
        return context
    

class LandingPageFilteredView(ListView):
    template_name = "landing_page.html"
    model = Campaign
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CampaignCategory.objects.all()
        if self.kwargs["pk"] != None:
            context["object_list"] = Campaign.objects.filter(category=self.kwargs["pk"]) 
        return context


class CampaignDetailsView(DetailView):
    template_name = "campaign_detail.html"
    model = Campaign

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["rewards"] = Reward.objects.filter(campaign=pk)
        context["comments"] = Comment.objects.filter(campaign=pk)
        return context


class ContributeView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "post_form.html"
    model = Contribution
    form_class = ContributionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.backer = self.request.user
        self.object.campaign = Campaign.objects.get(id=self.kwargs["camp_pk"])
        self.object.save()

        campaign = Campaign.objects.filter(id=self.kwargs["camp_pk"])
        campaign.update(current_amount=F('current_amount') + self.object.amount)

        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
          return reverse_lazy('campaign-details', kwargs={'pk': self.kwargs['camp_pk']})


class AddCommentView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "post_form.html"
    model = Comment
    form_class = CommentCreationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.campaign = Campaign.objects.filter(id=self.kwargs["camp_pk"]).first()
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)
    
    def get_success_url(self):
          return reverse_lazy('campaign-details', kwargs={'pk': self.kwargs['camp_pk']})
    

class CreateCampaignView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "post_form.html"
    model = Campaign
    form_class = CampaignCreationForm
    new_id = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.new_id = self.object.id
        return super(ModelFormMixin, self).form_valid(form)
    
    def get_success_url(self):
          return reverse_lazy('campaign-details', kwargs={'pk': self.new_id})
    

class SignUpView(FormView):
    template_name = "post_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    

class AccountView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        context["campaigns"] = Campaign.objects.filter(owner=self.request.user)
        context["pledges"] = Contribution.objects.filter(backer=self.request.user)
        context["comments"] = Comment.objects.filter(user=self.request.user)

        return context