from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context = {'boldmessage': 'a bold message'}
    return HttpResponse(render(request, 'rango/index.html', context))


def about(request):
    return HttpResponse('Rango says here is the about page')
