from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import URLPattern, URLResolver, get_resolver
from .models import Category, Product, Store, Promotion

class HomeView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:6]
        context['promotions'] = Promotion.objects.filter(is_active=True)[:3]
        return context

class CatalogView(ListView):
    model = Category
    template_name = 'store/catalog.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'store/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.filter(available=True)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'], category__slug=self.kwargs['category_slug'])

class StoreListView(ListView):
    model = Store
    template_name = 'store/store_list.html'
    context_object_name = 'stores'

class PromotionListView(ListView):
    model = Promotion
    template_name = 'store/promotions.html'
    context_object_name = 'promotions'

    def get_queryset(self):
        return Promotion.objects.filter(is_active=True)

class AboutView(TemplateView):
    template_name = 'store/about.html'

class ContactsView(TemplateView):
    template_name = 'store/contacts.html'

def toggle_theme(request):
    current = request.session.get('theme', 'default')
    request.session['theme'] = 'vi' if current == 'default' else 'default'
    return redirect(request.META.get('HTTP_REFERER', '/'))

class SitemapView(TemplateView):
    template_name = 'store/sitemap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls = []
        def extract_urls(urlpatterns, prefix=''):
            for pattern in urlpatterns:
                if isinstance(pattern, URLResolver):
                    extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                elif isinstance(pattern, URLPattern):
                    if pattern.name and 'admin' not in prefix:
                        urls.append({
                            'name': pattern.name,
                            'url': '/' + prefix + str(pattern.pattern).replace('^', '').replace('$', '')
                        })
        extract_urls(get_resolver().url_patterns)
        context['urls'] = urls
        return context

def custom_404(request, exception):
    return render(request, 'store/404.html', status=404)
