from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import URLPattern, URLResolver, get_resolver
from .models import Category, Product, Store, Promotion
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Article, Banner, ContactMessage
from .forms import ContactForm
from .forms import SearchForm
from .models import UserProfile
from .forms import UserForm, ProfileForm

class HomeView(TemplateView):
    template_name = 'store/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:6]
        context['promotions'] = Promotion.objects.filter(is_active=True)[:3]
        context['latest_articles'] = Article.objects.filter(is_published=True)[:5]
        context['search_form'] = SearchForm()
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
        # Ручное построение дерева страниц (можно расширить)
        sitemap_tree = [
            {
                'title': 'Главная',
                'url': 'home',
                'children': []
            },
            {
                'title': 'Каталог',
                'url': 'catalog',
                'children': [
                    {'title': 'Мягкая мебель', 'url': 'category_detail', 'slug': 'myagkaya-mebel', 'children': []},
                    {'title': 'Посуда', 'url': 'category_detail', 'slug': 'posuda', 'children': []},
                    {'title': 'Хранение', 'url': 'category_detail', 'slug': 'khranenie', 'children': []},
                    {'title': 'Товары для клининга', 'url': 'category_detail', 'slug': 'cleaning', 'children': []},
                ]
            },
            {
                'title': 'Статьи',
                'url': 'articles',
                'children': []
            },
            {
                'title': 'Магазины',
                'url': 'stores',
                'children': []
            },
            {
                'title': 'Акции',
                'url': 'promotions',
                'children': []
            },
            {
                'title': 'О нас',
                'url': 'about',
                'children': []
            },
            {
                'title': 'Контакты',
                'url': 'contacts',
                'children': []
            },
            {
                'title': 'Карта сайта',
                'url': 'sitemap',
                'children': []
            },
            {
                'title': 'Поиск',
                'url': 'search',
                'children': []
            },
            {
                'title': 'Вход / Регистрация',
                'url': 'login',
                'children': [
                    {'title': 'Войти', 'url': 'login', 'children': []},
                    {'title': 'Зарегистрироваться', 'url': 'register', 'children': []},
                ]
            },
            {
                'title': 'Личный кабинет',
                'url': 'profile',
                'children': []
            },
            {
                'title': 'Версия для слабовидящих',
                'url': 'toggle_theme',
                'children': []
            },
        ]
        context['sitemap'] = sitemap_tree
        return context

class ArticleListView(ListView):
    model = Article
    template_name = 'store/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'store/article_detail.html'
    context_object_name = 'article'

class SearchView(ListView):
    template_name = 'store/search_results.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            # Поиск
            products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), available=True)
            articles = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), is_published=True)

            results = list(products) + list(articles)

            for item in results:
                item.type = 'product' if isinstance(item, Product) else 'article'
            return results
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'store/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        UserProfile.objects.create(user=self.object)
        return response

def custom_404(request, exception):
    return render(request, 'store/404.html', status=404)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'store/contact_success.html')

def toggle_theme(request):
    current = request.session.get('theme', 'default')
    request.session['theme'] = 'vi' if current == 'default' else 'default'
    return redirect(request.META.get('HTTP_REFERER', '/'))

