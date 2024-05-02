import json


from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


from payment.serializers import CreatePaymentSerializer, CancelPaymentSerializer
from payment.services.payment_services import create_payment, payment_accept_or_cancel, cancel_payment


class CreatePaymentView(CreateAPIView):
    """
    post:
        Create a payment to user's order(products in the cart).
        Returns payment url(yookassa).
    """

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
    """
    post:
        Cancel the current payment to user's order(products in the cart).
        Returns products quantity in the shop.
        Returns response status 200 or 400.
    """

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
    """
    post:
        Only for Yookassa using. Get response from Yookassa.
        If payment is succeeded - complete the order.
        If payment is canceled - delete payment process,
        returns products quantity in the shop.
        Returns response status 200 or 400.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)
        if payment_accept_or_cancel(response):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
