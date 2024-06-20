from rest_framework import serializers


class GenericErrorSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    message = serializers.CharField(allow_null=True)


class ResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    status = serializers.CharField()
    recordsTotal = serializers.IntegerField()
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        data = instance.get('data')

        return data
