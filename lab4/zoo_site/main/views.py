from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Animal, Placement, Staffer
from django.http import Http404
import requests
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin


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

class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('personal_account')

    def get_object(self, queryset=None):
        return self.request.user

class AnimalCreate(CreateView):
    model = Animal
    fields = ['name', 'species', 'animal_class', 'country', 'placement', 'fodder',
              'admission_date', 'birth_date', 'image', 'info', 'daily_feed']
    success_url = reverse_lazy('user_animals')

    def form_valid(self, form):
        form.instance.staffer = Staffer.objects.filter(username=self.request.user.username).first()
        return super().form_valid(form)

class AnimalUpdate(UpdateView):
    model = Animal
    fields = ['placement', 'image', 'info', 'fodder', 'daily_feed']
    success_url = reverse_lazy('user_animals')

class AnimalDelete(DeleteView):
    model = Animal
    success_url = reverse_lazy('user_animals')

class PlacementCreate(CreateView):
    model = Placement
    fields = ['name', 'number', 'basin', 'area']
    success_url = reverse_lazy('user_placements')

    def form_valid(self, form):
        if Placement.objects.filter(name=form.cleaned_data['name'], number=form.cleaned_data['number']).exists():
            form.add_error(None, 'Placement with the same name and number already exists.')
            return self.form_invalid(form)

        return super().form_valid(form)

class PlacementUpdate(UpdateView):
    model = Placement
    fields = ['basin', 'area']
    success_url = reverse_lazy('user_placements')

class PlacementDelete(DeleteView):
    model = Placement
    success_url = reverse_lazy('user_placements')
