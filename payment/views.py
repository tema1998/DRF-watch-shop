import json

from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.serializers import CreatePaymentSerializer
from payment.services.payment_services import create_payment, payment_acceptance


class CreatePaymentView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serialized_data = serializer.validated_data
        else:
            return Response(serializer.errors)
        confirmation_url = create_payment(serialized_data)
        return Response({'confirmation_url': confirmation_url})


class AcceptPaymentView(CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)

        if payment_acceptance(response):
            return Response(200)
        return Response(404)
