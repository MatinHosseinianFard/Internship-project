from rest_framework import serializers

from .models import Benefactor
from .models import Charity, Task


class BenefactorSerializer(serializers.ModelSerializer):
    pass


class CharitySerializer(serializers.ModelSerializer):
    pass


class TaskSerializer(serializers.ModelSerializer):
    pass
