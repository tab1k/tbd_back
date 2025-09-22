from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=False, null=False)

    def __str__(self):
        if self.title:
            return self.title
        return f"Video {self.id}"

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title or f"Case {self.id}"

    class Meta:
        ordering = ['-created_at']

class CaseImage(models.Model):
    case = models.ForeignKey(Case, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='case_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.case.title or 'Case ' + str(self.case.id)}"

    class Meta:
        ordering = ['created_at']
