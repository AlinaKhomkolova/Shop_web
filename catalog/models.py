from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}\n'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images_products/', verbose_name='Изображение (превью)', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания (записи в БД)')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения (записи в БД)')

    def __str__(self):
        return f'{self.name}\n'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name', 'category', 'price', 'created_at',)


class ContactInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='E-mail')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания (записи в БД)')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('created_at',)

    def __str__(self):
        return f"Contact: {self.name}, {self.email}"


class Version(models.Model):
    product = models.ForeignKey(Product, verbose_name='Наименование продукта', on_delete=models.CASCADE,
                                related_name='versions', **NULLABLE)
    version_number = models.PositiveIntegerField(default='0', verbose_name='Номер версии',
                                                 help_text='Введите номер версии продукта', **NULLABLE)
    version_name = models.CharField(max_length=150, verbose_name='Название версии',
                                    help_text="Введите наименование версии продукта", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Признак текущей версии', help_text="Версия активна?",
                                    **NULLABLE)

    def __str__(self):
        return f'{self.version_name}\n'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('product', 'version_number', 'version_name',)
