from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CamperRegistrationSerializer, CampSerializer, CamperSerializer
from .models import *
import pdfplumber
import re
from datetime import datetime, date
from .permissions import *


@login_required(login_url="account_login")
def profile(request):
    return render(request, "profile.html")

@login_required(login_url='account_login')
def register_camper_page(request):
    from .models import Camp
    camps = Camp.objects.filter(is_active=True)
    return render(request, "campers/register_camper.html", {"camps": camps})


@login_required(login_url='account_login')
def my_campers(request):
    
    return render(request, "campers/my_campers.html")


class CreateCampAPI(generics.CreateAPIView):
    serializer_class = CampSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin, IsAdmin]

    def post(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        if serializer.is_valid():
            camps = serializer.save()
            return Response({
                "success": f"{len(camps) if many else 1} camp(s) created",
                "camps": CampSerializer(camps, many=many).data
            }, status=201)
        return Response({"errors": serializer.errors}, status=400)
    

class CampersView(generics.ListAPIView):
    serializer_class = CamperSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CamperRegister.objects.filter(parent=user)



class RegisterCamperAPI(generics.CreateAPIView):
    serializer_class = CamperRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        camper = serializer.save()
        return Response(
            {"success": f"Заявка на регистрацию ребёнка '{camper.full_name}' в лагерь '{camper.camp.name}' успешно создана"},
            status=status.HTTP_201_CREATED
        )