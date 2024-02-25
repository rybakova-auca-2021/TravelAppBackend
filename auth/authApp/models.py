from django.contrib.auth.models import User
from django.db import models

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
    name = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.ImageField(upload_to='main_images/')
    detail_images = models.ManyToManyField('DetailImage', blank=True)

    def __str__(self):
        return self.name

class DetailImage(models.Model):
    image = models.ImageField(upload_to='detail_images/')

    def __str__(self):
        return self.image.name

class PopularPlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

class MustVisitPlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    places = models.ManyToManyField(Place)

    def __str__(self):
        return self.name
