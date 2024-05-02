import json

from django.shortcuts import render

from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.serializers import CreatePaymentSerializer, CancelPaymentSerializer
from payment.services.payment_services import create_payment, payment_acceptance, cancel_payment


class CreatePaymentView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serialized_data = serializer.validated_data
        else:
            return Response(serializer.errors)
        payment_url = create_payment(serialized_data)
        if payment_url:
            return Response({'payment_url': payment_url})
        else:
            return Response("Error in moment of creating payment.", status=status.HTTP_400_BAD_REQUEST)


class CancelPaymentView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CancelPaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CancelPaymentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serialized_data = serializer.validated_data
        else:
            return Response(serializer.errors)
        cancel_status = cancel_payment(serialized_data)
        if cancel_status:
            return Response("The order payment was successfully canceled.", status=status.HTTP_200_OK)
        else:
            return Response("The order payment doesn't exist.", status=status.HTTP_400_BAD_REQUEST)


class AcceptPaymentView(CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)

        if payment_acceptance(response):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
