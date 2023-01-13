from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100, allow_null=True)
    firstname = serializers.CharField(max_length=100, allow_null=True)
    middlename = serializers.CharField(max_length=100, allow_null=True)

    shortname = serializers.SerializerMethodField()

    def get_shortname(self, obj):
        return obj.get_shortname()