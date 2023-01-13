from django.db import models

class Comment(models.Model):
    class Meta(object):
        app_label = 'nomenclature'