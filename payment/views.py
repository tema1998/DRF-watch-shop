from django.shortcuts import render

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.services.payment_services import create_payment


class CreatePaymentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        confirmation_url = create_payment()
        return Response({'confirmation_url': confirmation_url})
