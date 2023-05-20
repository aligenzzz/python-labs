from django.shortcuts import render
from django.views import generic
from .models import Animal, Placement, Staffer
from django.http import Http404, HttpResponse
import requests
from django.views import View


class HomeView(View):
    @staticmethod
    def get(request):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        image_url = response.json()['message']

        response = requests.get('https://catfact.ninja/fact')
        fact = response.json()['fact']

        context = {
            'image_url': image_url,
            'fact': fact
        }

        return render(request, 'main/index.html', context)


class AnimalListView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'


class AnimalDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            animal = Animal.objects.get(id=id)
        except Animal.DoesNotExist:
            raise Http404("Animal doesn't exist :(")

        return render(
            request,
            'main/animal_detail.html',
            context={'animal': animal, }
        )

class PlacementListView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

class PlacementDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            placement = Placement.objects.get(id=id)
        except Placement.DoesNotExist:
            raise Http404("Placement doesn't exist :(")

        return render(
            request,
            'main/placement_detail.html',
            context={'placement': placement, }
        )


class PlacementAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        id = self.kwargs['id']
        placement = Placement.objects.get(id=id)
        return Animal.objects.filter(placement=placement)


class StafferListView(generic.ListView):
    model = Staffer
    context_object_name = 'staff_list'
    template_name = 'main/staff.html'


class StafferDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            staffer = Staffer.objects.get(id=id)
        except Staffer.DoesNotExist:
            raise Http404("Staffer doesn't exist :(")

        return render(
            request,
            'main/staffer_detail.html',
            context={'staffer': staffer, }
        )

class StafferAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        id = self.kwargs['id']
        staffer = Staffer.objects.get(id=id)
        return Animal.objects.filter(staffer=staffer)


class StafferPlacementsView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

    def get_queryset(self):
        id = self.kwargs['id']
        staffer = Staffer.objects.get(id=id)
        return Placement.objects.filter(animals__in=staffer.animals.all()).distinct()

class PersonalAccountView(View):
    @staticmethod
    def get(request):
        return render(
            request,
            'main/personal.html',
        )

class UserProfileView(View):
    @staticmethod
    def get(request):
        try:
            staffer = Staffer.objects.get(username=request.user.username)
        except Staffer.DoesNotExist:
            raise Http404("Staffer doesn't exist :(")

        return render(
            request,
            'main/staffer_detail.html',
            context={'staffer': staffer, }
        )

class UserAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        staffer = Staffer.objects.get(username=self.request.user.username)
        return Animal.objects.filter(staffer=staffer)

class UserPlacementsView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

    def get_queryset(self):
        staffer = Staffer.objects.get(username=self.request.user.username)
        return Placement.objects.filter(animals__in=staffer.animals.all()).distinct()

class UserSettingsView(View):
    @staticmethod
    def get(request):
        return HttpResponse("SETTINGS")

