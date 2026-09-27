from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name
