from django.db import models
from slugify import slugify


class Specialization(models.Model):

    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)
