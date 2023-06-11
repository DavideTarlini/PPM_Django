from django.forms import ModelForm
from mainapp.models import Campaign, Comment, Contribution


class CampaignCreationForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ["title", "description", "image_url", "goal_amount", "start_date", "end_date", "category"]


class CommentCreationForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class ContributionForm(ModelForm):
    class Meta:
        model = Contribution
        fields = ["amount"]