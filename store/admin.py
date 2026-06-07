from django.contrib import admin
from .models import Category, Product, Store, Promotion
from .models import ArticleCategory, Article

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Promotion)
admin.site.register(ArticleCategory)
admin.site.register(Article)
