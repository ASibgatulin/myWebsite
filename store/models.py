from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    work_time = models.CharField(max_length=100)  # "09:00–21:00"
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.address}"

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статей'

    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Текст статьи')
    image = models.ImageField(upload_to='articles/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Banner(models.Model):
    POSITIONS = [
        ('home_top', 'Главная – верх'),
        ('home_bottom', 'Главная – низ'),
        ('sidebar', 'Сайдбар'),
    ]
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    position = models.CharField(max_length=20, choices=POSITIONS, default='home_top')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class ArticleCategory(models.Model):
        name = models.CharField(max_length=100, verbose_name='Название')
        slug = models.SlugField(unique=True)

        class Meta:
            verbose_name = 'Категория статьи'
            verbose_name_plural = 'Категории статей'

        def __str__(self):
            return self.name

    class Article(models.Model):
        category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles')
        title = models.CharField(max_length=200, verbose_name='Заголовок')
        slug = models.SlugField(unique=True)
        content = models.TextField(verbose_name='Текст статьи')
        image = models.ImageField(upload_to='articles/', blank=True, verbose_name='Изображение')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

        class Meta:
            verbose_name = 'Статья'
            verbose_name_plural = 'Статьи'
            ordering = ['-created_at']

        def __str__(self):
            return self.title

    class Banner(models.Model):
        POSITIONS = [
            ('home_top', 'Главная – верх'),
            ('home_bottom', 'Главная – низ'),
            ('sidebar', 'Сайдбар'),
        ]
        title = models.CharField(max_length=100)
        image = models.ImageField(upload_to='banners/')
        link = models.URLField(blank=True)
        position = models.CharField(max_length=20, choices=POSITIONS, default='home_top')
        is_active = models.BooleanField(default=True)
        order = models.PositiveIntegerField(default=0)

        class Meta:
            ordering = ['order']

        def __str__(self):
            return self.title

    class ContactMessage(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        phone = models.CharField(max_length=20, blank=True)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        is_processed = models.BooleanField(default=False)

        class Meta:
            verbose_name = 'Сообщение с сайта'
            verbose_name_plural = 'Сообщения с сайта'

        def __str__(self):
            return f'От {self.name} - {self.created_at.strftime("%d.%m.%Y")}'


