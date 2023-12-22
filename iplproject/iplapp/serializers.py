from rest_framework.serializers import ModelSerializer,Serializer
from iplapp.models import Franchises
from rest_framework import serializers

class FranchisesModelSerializer(ModelSerializer):
    class Meta:
        model = Franchises
        fields = "__all__"


class FranchesisNormalSerializer(Serializer):
    f_name = serializers.CharField(max_length=30)
    f_nickname = serializers.CharField(max_length=4)
    f_started_year = serializers.IntegerField()
    f_logo = serializers.ImageField(required=False)
    no_of_trophies = serializers.IntegerField()
