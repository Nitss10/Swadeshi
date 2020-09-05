from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Agent
from .serializer import AgentSerializer
# Create your views here.

class AgentListView(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
