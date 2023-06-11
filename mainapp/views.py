from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import DetailView, FormView, CreateView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from mainapp.forms import CampaignCreationForm, CommentCreationForm, ContributionForm
from mainapp.models import Campaign, Reward, Comment, Contribution


class LandingPageView(ListView):
    template_name = "landing_page.html"
    model = Campaign
    paginate_by = 20
    

class SignUpView(FormView):
    template_name = "post_form.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


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
    success_url = reverse_lazy("landing-page")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.backer = self.request.user
        self.object.campaign = Campaign.objects.get(id=self.kwargs["camp_pk"])
        self.object.save()

        Campaign.objects.filter(id=self.kwargs["camp_pk"]).update(current_amount = (self.object.amount+self.object.campaign.current_amount))
 

        return super(ModelFormMixin, self).form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "post_form.html"
    model = Comment
    form_class = CommentCreationForm
    success_url = reverse_lazy("landing-page")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.campaign = Campaign.objects.filter(id=self.kwargs["camp_pk"]).first()
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)
    

class CreateCampaignView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "post_form.html"
    model = Campaign
    form_class = CampaignCreationForm
    success_url = reverse_lazy("landing-page")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)
    

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