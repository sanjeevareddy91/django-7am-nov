from rest_framework.serializers import ModelSerializer
from iplapp.models import Franchises

class FranchisesModelSerializer(ModelSerializer):
    class Meta:
        model = Franchises
        fields = "__all__"