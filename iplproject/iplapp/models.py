from django.db import models

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