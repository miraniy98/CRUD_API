from django.db import models
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse

# Create your models here.
class BlogPost(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title   = models.CharField(max_length=120, null=True, blank=True)
    content = models.TextField(max_length=120, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return api_reverse("api-post:post-rud", kwargs={'pk' : self.pk}, request=request)
