import os
from datetime import datetime
import traceback
from pprint import pprint

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from financial.models import (
    Customer,
    Date,
    Payment,
    Plan
)


class PlanSerializer(serializers.ModelSerializer):

    plano = serializers.CharField(max_length=10)

    class Meta:
        model = Plan
        fields = ["plano"]
        ordering = ["id"]
    
    def create(self, validated_data):
        try:
            plan = Plan.objects.get(
                plano=validated_data.get('plano')
            )
            return plan
        except Plan.DoesNotExist:
            return super().create(validated_data)


class DateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Date
        fields = ["data", "mes", "ano"]
        ordering = ["data"]
    
    def create(self, validated_data):
        try:
            date = Date.objects.get(
                data=validated_data.get('data')
            )
            return date
        except Date.DoesNotExist:
            return super().create(validated_data)


class CustomerSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Customer
        fields = ["nome", "cidade", "estado", "segmento"]
        ordering = ["nome"]
    
    def create(self, validated_data):
        try:
            customer = Customer.objects.get(
                nome=validated_data.get('nome')
            )
            return customer
        except Customer.DoesNotExist:
            return super().create(validated_data)


class PaymentSerializer(WritableNestedModelSerializer):
    
    plan = PlanSerializer(required=True)
    date = DateSerializer(required=True)
    customer = CustomerSerializer(required=True)
    
    class Meta:
        model = Payment
        fields = ["plan", "date", "customer", "valor", "qtde_meses_pagos"]   
        ordering = ["-updated_at"]

    def create(self, validated_data):
        try:
            payment = Payment.objects.get(
                pk=validated_data.get('id'),
            )

            serializer = PlanSerializer(
                data=validated_data.get('plan')
            )
            if serializer.is_valid():
                plan = serializer.save()
                payment.plan.add(plan)
            
            serializer = DateSerializer(
                data=validated_data.get('date')
            )
            if serializer.is_valid():
                date = serializer.save()
                payment.date.add(date)
            
            serializer = CustomerSerializer(
                data=validated_data.get('customer')
            )
            if serializer.is_valid():
                customer = serializer.save()
                payment.customer.add(customer)
                payment.save()
            
            return payment

        except Payment.DoesNotExist:

            return super().create(validated_data)


from financial.models import Test
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

