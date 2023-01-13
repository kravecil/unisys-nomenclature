from rest_framework import serializers

from nomenclature.models.products import Product
from nomenclature.models.groups import Group
from nomenclature.models.units import Unit, UnitSerializer
from nomenclature.models.okpd import OkpdSerializer
from nomenclature.models.okved import OkvedSerializer
from nomenclature.models.ens import EnsSerializer

class ProductSerializer(serializers.ModelSerializer):
    # group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    unit_rel = serializers.SerializerMethodField()
    okpd_rel = serializers.SerializerMethodField()
    okved_rel = serializers.SerializerMethodField()
    ens_rel = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["pk", "name","number", "group", 'notes',
            'unit', 'okpd', 'okved', 'unit_rel', 'okpd_rel', 'okved_rel', 'ens', 'ens_rel']

    def get_unit_rel(self, obj):
        return UnitSerializer(obj.unit, many=False).data if obj.unit else None

    def get_okpd_rel(self, obj):
        return OkpdSerializer(obj.okpd, many=False).data if obj.okpd else None

    def get_okved_rel(self, obj):
        return OkvedSerializer(obj.okved, many=False).data if obj.okved else None

    def get_ens_rel(self, obj):
        return EnsSerializer(obj.ens, many=False).data if obj.ens else None