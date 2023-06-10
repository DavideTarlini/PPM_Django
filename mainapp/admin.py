from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CampaignCategory)
admin.site.register(Campaign)
admin.site.register(Reward)
admin.site.register(Comment)
admin.site.register(UpdateNotify)
admin.site.register(Contribution)