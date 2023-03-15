from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from stack.forms import SignupForm,LoginForm,QuestionForm,UserProfileForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from stack.models import Questions,Answers,UserProfile
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            return redirect('log-in')
        else:
            return fn(request,*args,**kw)
    return wrapper
decs=[signin_required,never_cache]


# Create your views here.
class SignupViews(CreateView):
    model=User
    template_name="signup.html"
    form_class=SignupForm
    success_url=reverse_lazy("log-in")

    




class LoginViews(View):
    def get(self,request,*args,**kw):
        form=LoginForm()
        return render(request,"login.html")


    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html")
@method_decorator(decs, name="dispatch")     
class IndexViews(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("home") 
    context_object_name="questions"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)  
    def get_queryset(self):
        
        return Questions.objects.all().order_by("-created_date")    
@method_decorator(decs, name="dispatch")  
class AddAnswersView(View):
    def post(self,request,*args,**kw):
        qid=kw.get("id")
        quest=Questions.objects.get(id=qid)
        usr=request.user
        ans=request.POST.get("answer")
        Answers.objects.create(user=usr,questions=quest,answer=ans)
        return redirect("home")
@method_decorator(decs, name="dispatch")  
class UpvoteViews(View):
    def get(self,request,*args,**kw):   
        id=kw.get("id")
        ans=Answers.objects.get(id=id)
        ans.upvote.add(request.user)
        ans.save()
        return redirect("home")
@method_decorator(decs, name="dispatch") 
class UserProfileCreateViews(CreateView):
    form_class=UserProfileForm
    template_name="profile-add.html"
    model=UserProfile
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
@method_decorator(decs, name="dispatch") 
class UserProfileViewing(TemplateView):
    template_name="profile-view.html"

@method_decorator(decs, name="dispatch") 
class UserProfileUpdateViews(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"
@method_decorator(decs, name="dispatch")  
class QuestionDeleteView(View):
    def get(self,request,*args,**kw):
        id=kw.get("pk")
        Questions.objects.get(id=id).delete()
        return redirect("home")
@method_decorator(decs, name="dispatch")  
class UpvoteRemoveViews(View):
    def get(self,request,*args,**kw):   
        id=kw.get("id")
        ans=Answers.objects.get(id=id)
        ans.upvote.remove(request.user)
        ans.save()
        return redirect("home")
@method_decorator(decs, name="dispatch") 
class SignoutView(View):
    def get(self,request,*args,**kw):
        logout(request)
        return redirect('log-in')







    

