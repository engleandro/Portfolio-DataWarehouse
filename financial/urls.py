from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .apiviews import (
    CustomerViewSets,
    DateViewSets,
    PaymentViewSets,
    PlanViewSets,
)


app = 'financial'

router = SimpleRouter()
router.register(r'plan', PlanViewSets)
router.register(r'date', DateViewSets)
router.register(r'customer', CustomerViewSets)
router.register(r'payment', PaymentViewSets)

urlpatterns = []
urlpatterns += router.urls


from .apiviews import TestViewSets
router.register(r'test', TestViewSets)
urlpatterns += router.urls

