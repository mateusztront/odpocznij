from django.shortcuts import render
from django.views import View
from main.models import Premises


class LandingPageView(View):
    def get(self, request):
        return render(request, 'landingpage.html')

class MainView(View):
    def get(self, request):
        search = request.GET.get('search')
        results = Premises.objects.all().filter(city=search)
        return render(request, 'main.html', {'results': results})
