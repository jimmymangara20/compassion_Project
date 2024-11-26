from django.db import models


# Create your models here.
class Forms(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    age = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    Religion = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# XAMPP
class UploadedImage(models.Model):
    title = models.CharField(max_length=100)#Title for the image
    image = models.ImageField(upload_to='Uploaded_images/') #Save images to this
    def __str__(self):
        return self.title