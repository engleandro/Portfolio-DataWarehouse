from rest_framework.response import Response
from rest_framework import views, viewsets

from .models import (
    Customer,
    Date,
    Plan,
    Payment
)
from .serializers import (
    CustomerSerializer,
    DateSerializer,
    PlanSerializer,
    PaymentSerializer
)


class PlanViewSets(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class CustomerViewSets(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DateViewSets(viewsets.ModelViewSet):
    queryset = Date.objects.all()
    serializer_class = DateSerializer


class PaymentViewSets(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class MonthlyRecurringRevenue(views.APIView):

    def get(self, request, format=None):
        payload = request.json
        usernames = [
            user.username \
                for user in Payment.objects.all()
                #for user in Payment.objects.filter(customer__id=payload.get('id'))
        ]
        return Response(usernames)


from .models import Test
from .serializers import TestSerializer

class TestViewSets(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

