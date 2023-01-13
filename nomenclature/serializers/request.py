from rest_framework import serializers
from rest_framework.response import Response
from nomenclature.serializers.generic_request import GenericRequestSerializer
from nomenclature.models.requests import Request
from nomenclature.models.approvements import Approvement
# from nomenclature.models import Product
# from nomenclature.models import Person
from nomenclature.serializers.product import ProductSerializer
from nomenclature.serializers.person import PersonSerializer
from nomenclature.serializers.approver import ApproverSerializer
from nomenclature.models.approvements import ApprovementSerializer

class RequestSerializer(GenericRequestSerializer):
    person_who_created = serializers.SerializerMethodField()
    # approvers_list = serializers.SerializerMethodField(required=False)
    approvements = serializers.SerializerMethodField()
    approvers_left = serializers.SerializerMethodField()
    approvers_all = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ["pk", "created_at", "approved_at",
                  "product", 'person_who_created',
                  'approvements',
                  'approvers_left',
                  'approvers_all',
                  ]

    def get_person_who_created(self, obj):
        person = obj.get_person_who_created()
        return PersonSerializer(person).data if person else None

    # def get_approvers_list(self, obj):
    #     approvers_list = self.context['approvers_list'] if 'approvers_list' in self.context else None
    #     return ApproverSerializer(approvers_list, many=True, read_only=True).data if approvers_list else None

    def get_approvements(self, obj):
        queryset = self.context['approvements'] if 'approvements' in self.context else None
        serializer = ApprovementSerializer(queryset, many=True)
        return serializer.data

    def get_approvers_left(self, obj):
        queryset = self.context['approvers_left'] if 'approvers_left' in self.context else None
        serializer = ApproverSerializer(queryset, many=True)
        return serializer.data

    def get_approvers_all(self, obj):
        queryset = self.context['approvers_all'] if 'approvers_all' in self.context else None
        serializer = ApproverSerializer(queryset, many=True)
        return serializer.data