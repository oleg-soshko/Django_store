from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category/')

    def get_absolute_url(self):
        return reverse('product_list', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    main_image = models.ImageField(upload_to='products/')
    slug = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField(default=False)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.category.slug, "product_slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)

    def __str__(self):
        return f'Изображение {self.product.name}'

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'


class Payment(models.Model):
    type = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Тип оплаты'
        verbose_name_plural = 'Типы оплаты'


class Delivery(models.Model):
    type = models.CharField(max_length=250)
    cost = models.FloatField()

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставки'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    payment_type = models.ForeignKey(Payment, verbose_name='Тип оплаты', on_delete=models.SET_NULL, null=True)
    delivery_type = models.ForeignKey(Delivery, verbose_name='Тип доставки', on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField()
    total_to_pay = models.FloatField()

    def __str__(self):
        return f'Заказ № {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetails(models.Model):
    product = models.ForeignKey(Product, verbose_name='Имя продукта', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Детали заказа № {self.order.pk}'

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'


class ProductReview(models.Model):
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Отзыв о продукте {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв о продукте'
        verbose_name_plural = 'Отзывы о продукте'


class OrderReview(models.Model):
    user = models.ForeignKey(User, verbose_name='Имя пользователя', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Отзыв о заказе № {self.order.pk}'

    class Meta:
        verbose_name = 'Отзыв о заказе'
        verbose_name_plural = 'Отзывы о заказе'


class RatingStars(models.Model):
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Звезды рейтинга'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    product = models.ForeignKey(Product, verbose_name='', on_delete=models.CASCADE)
    rating_stars = models.ForeignKey(RatingStars, verbose_name='', on_delete=models.CASCADE)

    def __str__(self):
        return f'Рейтинг'

    class Meta:
        verbose_name = 'Рейтинг продукта'
        verbose_name_plural = 'Рейтинг продукта'
