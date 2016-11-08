from django.db import models


class Cycle(models.Model):
    name = models.CharField(max_length=128, null=False)