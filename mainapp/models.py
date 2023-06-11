from django.db import models
from django.contrib.auth.models import User


class CampaignCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "CampaignCategory"

    def __str__(self):
        return self.name


class Campaign(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url =models.URLField(default="https://static.vecteezy.com/system/resources/previews/005/337/799/original/icon-image-not-found-free-vector.jpg")
    goal_amount = models.DecimalField(max_digits=10, decimal_places=0)
    current_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CampaignCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Campaign"

    def __str__(self):
        return self.title


class Reward(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    minimum_pledge = models.DecimalField(max_digits=10, decimal_places=0)
    estimated_delivery = models.DateField()

    class Meta:
        db_table = "Reward"

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Comment"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.campaign.title}"


class Contribution(models.Model):
    backer = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Contribution"

    def __str__(self):
        return f"{self.backer.username} backed {self.campaign.title}"