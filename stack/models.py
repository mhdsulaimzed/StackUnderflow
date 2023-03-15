
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
class Questions(models.Model):
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    class Meta:
        ordering=["-created_date"]

    def __str__(self):
        return self.description
    @property
    def question_answers(self):
        return Answers.objects.filter(questions=self).annotate(ucount=Count('upvote')).order_by('-ucount')

class Answers(models.Model):
    answer=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    questions=models.ForeignKey(Questions,on_delete=models.CASCADE)
    upvote=models.ManyToManyField(User,related_name="ans")
    created_date=models.DateField(auto_now_add=True)
    @property
    def upvote_count(self):
        return self.upvote.all().count()

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profiles",null=True)
    bio=models.CharField(max_length=50)
    @property
    def question_count(self):
        return Questions.objects.filter(user=self.user).count()



