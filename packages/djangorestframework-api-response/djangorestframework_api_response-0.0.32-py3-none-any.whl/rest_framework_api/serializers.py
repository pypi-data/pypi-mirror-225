from rest_framework import serializers


class APIResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    status = serializers.IntegerField(required=False)
    results = serializers.JSONField(required=False)
    extra_data = serializers.JSONField(required=False)
    count = serializers.IntegerField(required=False)
    next = serializers.URLField(required=False)
    previous = serializers.URLField(required=False)
    error = serializers.CharField(required=False)
