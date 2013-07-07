from django.views import generic as generic_views


class HomeView(generic_views.TemplateView):
    template_name = 'frontend/home.html'
