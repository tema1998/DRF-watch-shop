from django.urls import path, include

from payment.views import CreatePaymentView, AcceptPaymentView, CancelPaymentView

app_name = 'payment'

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create_payment"),
    path("cancel/", CancelPaymentView.as_view(), name="cancel_payment"),
    path("accept/", AcceptPaymentView.as_view(), name="accept_payment"),
]