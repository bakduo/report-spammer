from rest_framework import serializers

from spammers.models import SpamMessage

class SpamMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamMessage
        fields = ("email","domain","state","time")

class SpamMessageSerializerWithID(serializers.ModelSerializer):
    class Meta:
        model = SpamMessage
        fields = '__all__'