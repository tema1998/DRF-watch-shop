from django.urls import path, include

from payment.views import CreatePaymentView, AcceptPaymentView

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create_payment"),
    path("accept/", AcceptPaymentView.as_view(), name="accept_payment"),
]