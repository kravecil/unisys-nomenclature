from django.db import models
from rest_framework import serializers
from nomenclature.serializers.approver import ApproverSerializer

class Approvement(models.Model):
    approver = models.ForeignKey('nomenclature.Approver', on_delete=models.CASCADE)
    request = models.ForeignKey('nomenclature.Request', on_delete=models.CASCADE)
    
    approved_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
    comment = models.TextField(blank=True)

    @property
    def state(self):
        if self.approved_at: return 1
        elif self.rejected_at: return -1
        else: return 0

class ApprovementSerializer(serializers.ModelSerializer):
    approver = ApproverSerializer()
    class Meta:
        model = Approvement
        fields = ['approved_at', 'rejected_at', 'comment', 'approver', 'state']
        read_only_fields = ['state']