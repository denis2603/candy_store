from django.db import models


class Categories(models.Model):

    title = models.CharField(max_length=150, unique=True, verbose_name='наименование категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):

    category = models.ForeignKey(Categories, on_delete=models.RESTRICT, verbose_name='категория')
    name = models.CharField(max_length=150, verbose_name='наименование продукта')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='цена')
    foto = models.ImageField(upload_to='foto/', verbose_name='изображение')

