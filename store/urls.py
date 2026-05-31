from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('catalog/<slug:category_slug>/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('stores/', views.StoreListView.as_view(), name='stores'),
    path('promotions/', views.PromotionListView.as_view(), name='promotions'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]
