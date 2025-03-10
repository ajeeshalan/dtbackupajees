from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
# Default User model
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField
#tags
from taggit.managers import TaggableManager

# Create your models here.

# Author Model
class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default="default-profile-pic.png", upload_to='uploads/profile-pictures', null=True)

    def _str_(self):
        return self.user.username

# Ads Model
class Ads(models.Model):
    
    CONDITION = (
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = RichTextField()
    prize = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True) 
    entry = models.CharField(max_length=100, choices=CONDITION)
    registeration_url = models.CharField(max_length=200)
    no_of_slots = models.CharField(max_length=200)
    video = EmbedVideoField(null=True, blank=True) 
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    img_link= models.CharField(max_length=1000)
    tags=TaggableManager()

    class Meta:
        verbose_name_plural = "Classified Ads"

    def _str_(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dashboard')
      
# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='uploads/category', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from category name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def _str_(self):
        return self.category_name

# Image Model
class AdsImages(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='uploads/%Y/%m/%d', default=None)

    def _str_(self):
        return self.ads.title

    class Meta:
        verbose_name_plural = 'Classified Ads Images'

# Top Banner Model
class AdsTopBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    banner_img_url = models.CharField(max_length=200, default="Place Your Banner Link", blank=True)
    #image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)
    url = models.CharField(max_length=200, default="Enter the Url", blank=True)

    def _str_(self):
        return self.title

# Right Banner Model
class AdsRightBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)

    def _str_(self):
        return self.title

# Bottom Banner Model
class AdsBottomBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)

    def _str_(self):
        return self.title