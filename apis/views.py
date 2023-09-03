from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from spammers.models import SpamMessage
from .serializers import SpamMessageSerializer, SpamMessageSerializerWithID


class APIListSpamMessage(generics.ListAPIView):
    queryset = SpamMessage.objects.all()
    serializer_class = SpamMessageSerializer

class APIDetailSpamMessage(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SpamMessage.objects.all()
    serializer_class = SpamMessageSerializerWithID
