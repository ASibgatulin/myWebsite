def theme_context(request):
    return {'theme': request.session.get('theme', 'default')}
