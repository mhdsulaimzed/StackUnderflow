from django.urls import path
from stack import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("stack/signup",views.SignupViews.as_view(),name="sign-up"),
    path('stack/signin',views.LoginViews.as_view(), name="log-in"),
    path("stack/home",views.IndexViews.as_view(),name="home"),
    path("stack/questions/<int:id>/answers/add",views.AddAnswersView.as_view(),name="add-ans"),
    path("stack/answer/<int:id>/upvote/add",views.UpvoteViews.as_view(),name="upvote"),
    path("stack/userprofile/add",views.UserProfileCreateViews.as_view(),name="profile-add"),
    path("stack/userprofile/view",views.UserProfileViewing.as_view(),name="profile-view"),
    path("stack/userprofile/<int:id>/edit",views.UserProfileUpdateViews.as_view(),name="profile-edit"),
    path("stack/question/<int:pk>/remove",views.QuestionDeleteView.as_view(),name="quesdel"),
    path("stack/answer/<int:id>/upvote/remove",views.UpvoteRemoveViews.as_view(),name="upvote-remove"),
    path('stack/logout',views.SignoutView.as_view(), name="log-out")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)