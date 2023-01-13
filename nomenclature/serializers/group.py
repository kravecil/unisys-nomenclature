from rest_framework import serializers
from nomenclature.models.groups import Group

class GroupSerializer(serializers.ModelSerializer):
    parent_group = serializers.PrimaryKeyRelatedField(many=False,read_only=True)
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ["pk", "name", "parent_group", 'children']
        # depth = 10

    def get_children(self, obj):
        return GroupSerializer(obj.children.all(), many=True).data if obj.children.count() > 0 else None