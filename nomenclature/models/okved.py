from django.db import models
from rest_framework import serializers

class Okved(models.Model):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.TextField()

class OkvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Okved
        fields = ['code', 'name']