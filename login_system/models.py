from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=200)
    passwordResetCode = models.CharField(max_length=200,null=True, blank=True)
    passwordResetCodeTime = models.DateTimeField( null=True, blank= True)


    def __str__(self):
        return "%s  %s  %s"%(self.name, self.email, self.password)