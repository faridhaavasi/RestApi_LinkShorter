from django.db import models
import string, random
from django.contrib.auth import get_user_model

user = get_user_model()

class Link(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='links')
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)

    def generate_short_code(self):
        length = 6
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
      
    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
