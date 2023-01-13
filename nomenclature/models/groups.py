from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)
    parent_group = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,related_name='children')

    class Meta(object):
        app_label = 'nomenclature'
        ordering = ['name']
