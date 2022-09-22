from django.db import models

# import vk_bot.bot
from pathlib import Path
from candy_store.settings import BASE_DIR


class Categories(models.Model):

    title = models.CharField(max_length=150, unique=True, verbose_name='наименование категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Product(models.Model):

    category = models.ForeignKey(Categories, on_delete=models.RESTRICT, verbose_name='категория')
    name = models.CharField(max_length=150, verbose_name='наименование продукта')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='цена')
    foto = models.ImageField(upload_to='foto/', verbose_name='изображение')
    id_foto_vk = models.CharField(max_length=32, verbose_name='id товара в VK', blank=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        from vk_bot.bot import bot_candy

        origin_foto_name = Product.objects.get(pk=self.pk).foto.name if self.pk else ''

        super().save(*args, **kwargs)

        if origin_foto_name != self.foto.name:
            path_to_foto = Path(BASE_DIR) / self.foto.name
            self.id_foto_vk = bot_candy.add_foto_to_vk(path_to_foto.as_posix())
            super().save(*args, **kwargs)
