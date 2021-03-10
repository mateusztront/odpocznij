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


class PremisesView(View):
    def get(self, request, id):
        premises = Premises.objects.get(pk=id)
        room_types = premises.rooms.order_by('people_number')
        return render(request, "premises_view.html", {"premises": premises, "room_types": room_types})
