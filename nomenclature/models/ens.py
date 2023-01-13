from django.db import models
from rest_framework import serializers

class Ens(models.Model):
    number = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=150)
    unit = models.CharField(max_length=10)
    okpd = models.CharField(max_length=20)
    okved = models.CharField(max_length=20)
    notes = models.TextField()

class EnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ens
        fields = ['number', 'name', 'unit', 'okpd', 'okved', 'notes']