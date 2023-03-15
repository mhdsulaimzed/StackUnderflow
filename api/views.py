from django.shortcuts import render
from rest_framework.response import Response
from rest_framework .viewsets import ModelViewSet, GenericViewSet
from api .serializers import UserSerializer, UserProfileSerializer, Questionserializer, AnswerSerializer
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from stack.models import UserProfile, Questions, Answers
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework import serializers


# Create your views here.
class UserView(GenericViewSet, CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    # def list(self,request,*args,**kw):
    #     qs=UserProfile.objects.get(user=request.user)
    #     sz=UserProfileSerializer(qs, many=False)
    #     return Response(data=sz.data)

    # can update quesry set
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        
        prof=self.get_object()
        if prof.user != request.user:
            return serializers.ValidationError("method not allowed")
        else:
            return super().destroy(request,)


class QuestionView(ModelViewSet):
    serializer_class = Questionserializer
    queryset = Questions.objects.all()
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return Questions.objects.all().order_by("-created_date")

    # instead we changed the model and add a meta class with ordering=["-created_date"]
    @action(methods=["post"], detail=True)
    def add_answer(self, request, *args, **kw):
        sz = AnswerSerializer(data=request.data)
        user = request.user
        quest = self.get_object()
        if sz.is_valid():
            sz.save(user=user, questions=quest)
            return Response(data=sz.data)
        else:
            return Response(data=sz.errors)

    # localhost:8000/api/answer/1


class AnswersView(ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")

    # localhost:8000/api/answers/1/add_upvote/
    @action(methods=["post"], detail=True)
    def add_upvote(self, request, *args, **kw):
        id = kw.get("pk")
        ans = Answers.objects.get(id=id)
        ans.upvote.add(request.user)
        ans.save()
        return Response(data="up=voted")

    @action(methods=["post"], detail=True)
    def down_upvote(self, request, *args, **kw):
        id = kw.get("pk")
        ans = Answers.objects.get(id=id)

        ans.upvote.remove(request.user)
        ans.save()
        return Response(data="down-voted")
