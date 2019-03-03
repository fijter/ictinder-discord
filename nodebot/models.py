from django.db import models

class Message(models.Model):
    discord_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
