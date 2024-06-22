from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    salary = models.IntegerField(null=True)
    experience = models.IntegerField(null=True)
    location = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    CATEGORY = (
        ('Male', 'male'),
        ('Female', 'female'),
        ('Other', 'other'),
    )

    name = models.CharField(max_length=200)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=200, choices=CATEGORY)
    mobile = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    resume = models.FileField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class CompanyAd(models.Model):
    image = models.ImageField(upload_to='company_ads/')
    company_name = models.CharField(max_length=255)
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.company_name
