import random
import os
from django.db import models

from django.db.models import Q
from django.db.models.signals import pre_save,post_save

from eth.utils import unique_slug_generator

from django.urls import reverse
# Create your models here.
def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext	


def upload_image_path(instance, filename):
	#print(instance)
	#print(filename)
	new_filename = random.randint(1,3493492323)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return "products/{new_filename}/{final_filename}".format(new_filename= new_filename, final_filename = final_filename)

class ProductQuerySet(models.query.QuerySet):
	def featured(self):
		return self.filter(featured= True)
	
	def active(self):
		return self.filter(active=True)

	def search(self, query):
		lookups = (	Q(title__icontains=query) |
					Q(description__icontains=query) | 
					Q(price__icontains=query) |
					Q(tag__title__icontains=query) |
					Q(tag__slug=query)
				)
		#Q(tag__name__icontains=query)
		# tshirt, t-shirt, t shirt
		return self.filter(lookups).distinct()


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using= self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self):
		return self.get_queryset().featured()

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)  #product.objects == self.get_queryset()
		if qs.count() == 1:
			return qs.first()
		return None 

	def search(self, query):
		return self.get_queryset().active().search(query)

class Product(models.Model):
	title		= models.CharField(max_length=120)
	slug		= models.SlugField(blank= True, unique= True)
	description	= models.TextField()
	price		= models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	image		= models.ImageField(upload_to=upload_image_path, null= True, blank= True)
	featured	= models.BooleanField(default=False)
	active 		= models.BooleanField(default=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	#image		= models.FileField(upload_to=upload_image_path, null= True, blank= True)
	#image2		= models.URLField(max_length= 500, null= True, blank= True)

	objects = ProductManager()

	def get_absolute_url(self):
		#return "/products/{slug}/".format(slug=self.slug)
		return reverse("shopping:detail", kwargs={"slug": self.slug})

	def __str__(self):            #for object description in python3
		return self.title

	def __unicode__(self):        #for object description in python
		return self.title

	@property 
	def name(self):
		return self.title

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)


# class Product(models.Model):
# 	category		= models.CharField(max_length=120)
# 	class category(models.Model):
# 		title		= models.CharField(max_length=120)
# 		slug		= models.SlugField(blank= True, unique= True)
# 		description	= models.TextField()
# 		price		= models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
# 		image		= models.ImageField(upload_to=upload_image_path, null= True, blank= True)
# 		featured	= models.BooleanField(default=False)
# 		active 		= models.BooleanField(default=True)
