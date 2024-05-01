from django.core.validators import MinValueValidator
from rest_framework import serializers

from core.models import Order


class CreatePaymentSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].default = serializers.CurrentUserDefault()
        self.fields["user"].required = False

    user = serializers.CharField()
    return_url = serializers.URLField()

    def validate(self, data):
        order = Order.objects.filter(
            user=data["user"],
            is_ordered=False,
        )
        if not order:
            raise serializers.ValidationError("There is no active order. Add products to your Cart to create order.")
        else:
            return data

