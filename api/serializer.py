from rest_framework import serializers
from .models import Subscribe_model

class Subscriber_serializer(serializers.ModelSerializer):
    """Client details serializer"""

    class Meta:
        model = Subscribe_model
        fields = "__all__"

    