from store.models import Banner

def banners_context(request):
    return {
        'banners_top': Banner.objects.filter(position='home_top', is_active=True),
        'banners_bottom': Banner.objects.filter(position='home_bottom', is_active=True),
        'banners_sidebar': Banner.objects.filter(position='sidebar', is_active=True),
    }

def theme_context(request):
    return {'theme': request.session.get('theme', 'default')}
