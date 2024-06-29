from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_used_extension_count(self):
        return self.used_extensions.count()

    def get_unused_extension_count(self):
        return self.unused_extensions.count()


class UsedExtension(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='used_extensions', on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)  # Modifié en CharField
    position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and UsedExtension.objects.filter(name=self.name, department=self.department).exists():
            # Une extension avec le même nom existe déjà dans ce département
            raise ValueError("Une extension avec ce nom existe déjà dans ce département.")
        return super().save(*args, **kwargs)


class UnusedExtension(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='unused_extensions', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and UnusedExtension.objects.filter(name=self.name, department=self.department).exists():
            # Une extension non utilisée avec le même nom existe déjà dans ce département
            raise ValueError("Une extension non utilisée avec ce nom existe déjà dans ce département.")
        return super().save(*args, **kwargs)
