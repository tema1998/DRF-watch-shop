from django.urls import path, include

from payment.views import CreatePaymentView

urlpatterns = [
    path("create/", CreatePaymentView.as_view(), name="create_payment"),

]