from django.db import models
from rest_framework import serializers

class Unit(models.Model):
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=10)
    codename = models.CharField(max_length=10)
    shortname_international = models.CharField(max_length=10)
    codename_international = models.CharField(max_length=10)

    class Meta(object):
        app_label = 'nomenclature'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['code', 'name', 'shortname', 'codename',
            'shortname_international', 'codename_international']
        extra_kwargs = {
            'code': {'validators': []},
        }