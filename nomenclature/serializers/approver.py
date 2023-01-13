from rest_framework import serializers
from nomenclature.models.approvers import Approver
from nomenclature.models.persons import Person
from nomenclature.serializers.person import PersonSerializer

class ApproverSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = Approver
        fields = ['person']

    def get_person(self, obj):
        person = Person(obj.auth_id)
        return PersonSerializer(person).data if person else None