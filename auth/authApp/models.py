from django.contrib.auth.models import User
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('category1', 'Popular places'),
        ('category2', 'Must Visit Places'),
        ('category3', 'Packages'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.CharField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')  

    def __str__(self):
        return self.name


class DetailImage(models.Model):
    image = models.ImageField(upload_to='detail_images/')

    def __str__(self):
        return self.image.name

class PopularPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=455, null=True)
    main_image = models.CharField(null=True)

    def __str__(self):
        return self.name

class MustVisitPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=455, null=True)
    main_image = models.CharField(null=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    main_image = models.CharField(default='')

    def __str__(self):
        return self.name

class SavedPlace(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    description = models.TextField()  
    main_image = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}'s saved place"