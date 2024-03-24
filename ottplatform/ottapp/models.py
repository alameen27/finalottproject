# models.py
from django.db import models



 
from unicodedata import name
from django.db import models

# Create your models here.
class movie(models.Model):
    customer_profile = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    Duration = models.CharField(max_length=50,default='')
    Genre= models.CharField(max_length=100,default='')
    Director=models.CharField(max_length=100,default='')
    year = models.CharField(max_length=100)
    desc = models.TextField(default='')  # Set default value to an empty string
    link = models.URLField(default='')
    rating = models.FloatField()
    image = models.ImageField(upload_to='media/', default='')

    def __str__(self):
        return self.name

class CustomerProfileImage(models.Model):
    customer_profile = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', default='default_image.jpg')


class series(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    desc = models.CharField(max_length=500)
    url= models.CharField(max_length=500)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class upcoming(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    desc = models.CharField(max_length=500)
    url= models.CharField(max_length=500)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class chromovies(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    desc = models.CharField(max_length=500)
    url= models.CharField(max_length=500)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)


class newlatest(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    directer = models.CharField(max_length=50)
    long = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    sdesc = models.CharField(max_length=500)
    ldesc = models.CharField(max_length=1000)
    url= models.CharField(max_length=1000)
    svedio =  models.CharField(max_length=1000)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class newmovie(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    directer = models.CharField(max_length=50)
    long = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    sdesc = models.CharField(max_length=500)
    ldesc = models.CharField(max_length=1000)
    url= models.CharField(max_length=1000)
    svedio =  models.CharField(max_length=1000)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class newseries(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    directer = models.CharField(max_length=50)
    long = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    sdesc = models.CharField(max_length=500)
    ldesc = models.CharField(max_length=1000)
    url= models.CharField(max_length=1000)
    svedio =  models.CharField(max_length=1000)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class newupcoming(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    directer = models.CharField(max_length=50)
    long = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    sdesc = models.CharField(max_length=500)
    ldesc = models.CharField(max_length=500)
    url= models.CharField(max_length=500)
    svedio =  models.CharField(max_length=500)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)

class newchromovies(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    directer = models.CharField(max_length=50)
    long = models.CharField(max_length=500)
    genre = models.CharField(max_length=500)
    sdesc = models.CharField(max_length=500)
    ldesc = models.CharField(max_length=500)
    url= models.CharField(max_length=500)
    svedio =  models.CharField(max_length=500)
    rating = models.FloatField()
    image1 = models.CharField( max_length=500)
    image2 = models.CharField( max_length=500)
    image3 = models.CharField( max_length=500)
    image4 = models.CharField( max_length=500)




class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # You should use a more secure way to store passwords
    DoB = models.DateField()
    phonenumber = models.CharField(max_length=15)  # Adjust max_length as needed

class CustomerProfile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='profile')
    profilename = models.CharField(max_length=50)
    pin = models.CharField(max_length=4)  
    avatar = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.profilename

class KidProfile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='kid_profiles')
    profilename = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.profilename

class moviekid(models.Model):
    kid_profile = models.ForeignKey(KidProfile, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    description = models.TextField()
    poster = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.title
    
class waste(models.Model):
    logo = models.ImageField(upload_to='waste/')


class upcoming(models.Model):
    name = models.CharField(max_length=50)
    Duration = models.CharField(max_length=50,default='')
    Genre= models.CharField(max_length=100,default='')
    Director=models.CharField(max_length=100,default='')
    year = models.PositiveIntegerField()
    desc = models.TextField(default='')  # Set default value to an empty string
    link = models.URLField(default='')
    image = models.ImageField(upload_to='media/', default='')

    def __str__(self):
        return self.name
    