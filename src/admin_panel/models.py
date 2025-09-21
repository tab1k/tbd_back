from django.db import models

class Requests(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 

    def __str__(self):
        return f'Новая заявка: {self.name} - {self.phone}'