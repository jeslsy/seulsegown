from django.db import models

# Create your models here.
'''1. Category (업종)'''
class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return f'제목 : {self.category_name}'


'''2. Brand(브랜드)'''
class Brand(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=200)

    def __str__(self):
        return f'[{self.category.category_name}] {self.brand_name}'


'''3. Jumpo(점포)'''
class Jumpo(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    jumpo_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    latitide = models.FloatField(default=0)
    logitude = models.FloatField(default=0)
    tel = models.CharField(max_length=200)

    def __str__(self):
        return f'[{self.brand.brand_name}] {self.jumpo_name}'