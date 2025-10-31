from rest_framework import serializers
from royaloutfit.models import TestImageTable


class TestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImageTable
        fields = ['image'] 

