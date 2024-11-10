from django.db import models
from django.contrib.auth import get_user_model
from apps.shorter.models import Link



user = get_user_model()

class Account(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name='account', unique=True)
    links = models.ForeignKey(Link, on_delete=models.CASCADE,related_name='links', null=True, blank=True)
    bio = models.CharField(max_length=120 ,blank=True, null=True)
    id_user = models.CharField(max_length=120, blank=True, null=True, unique=True, db_index=True)

    def __str__(self) -> str:
        return f'account user: {self.user}'
    
    
