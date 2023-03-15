from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

from rest_framework_simple_jwt import TokenObtainPairView,TokenRefreshView
router=DefaultRouter()
router.register("acc/users",views.UserView,basename="users")
router.register("acc/users/profile",views.ProfileView,basename="userpro")
router.register("acc/questions",views.QuestionView,basename="userpro")
router.register("acc/answer",views.AnswersView,basename="answers")

urlpatterns = [
    path("token/",TokenObtainPairView.as_view(),name='tokens'),
    path("token/refresh",TokenRefreshView.as_view(),name='tokens-ref')

    
    
]+router.urls

#105b6a9c6ba9582588af911cff6f72ca33667455  flask user token