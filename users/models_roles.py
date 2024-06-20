from django.db import models


class Role(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.CharField(max_length=255, null=True)
    updated_by = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
