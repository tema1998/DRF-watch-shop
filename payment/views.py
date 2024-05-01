import json

from django.shortcuts import render

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.services.payment_services import create_payment, payment_acceptance


class CreatePaymentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        confirmation_url = create_payment()
        return Response({'confirmation_url': confirmation_url})


class AcceptPaymentView(CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)
        print(response)

        if payment_acceptance(response):
            return Response(200)
        return Response(404)
