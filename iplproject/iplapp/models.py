from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Franchises(models.Model):
    f_name = models.CharField(max_length=30)
    f_nickname = models.CharField(max_length=4)
    f_started_year = models.IntegerField()
    f_logo = models.ImageField(upload_to='logos',blank=True,null=True)
    no_of_trophies = models.IntegerField()

    def __str__(self):
        return self.f_name
    
    class Meta:
        db_table = 'franchises'

class UserInfo(models.Model):
    user_data = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    otp = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.mobile
    
class Schedule(models.Model):
    team1 = models.CharField(max_length=4)
    team2 = models.CharField(max_length=4)
    winner = models.CharField(max_length=4,null=True,blank=True)

    def __str__(self):
        return str(self.team1)+ 'Vs' +str(self.team2)