from django.db import models
from rest_framework import serializers

class Okpd(models.Model):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.TextField()

class OkpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Okpd
        fields = ['code', 'name']