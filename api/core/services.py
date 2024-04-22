from rest_framework import serializers


def validator_of_discount(value):
    if value < 0 or value > 100:
        raise serializers.ValidationError('Discount must be 0-100')
