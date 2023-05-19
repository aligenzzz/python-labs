from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')

def animals(request):
    return HttpResponse("ANIMALS")

def placements(request):
    return HttpResponse("PLACEMENTS")