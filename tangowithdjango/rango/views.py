from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def index(request):
    qs = Category.objects.order_by('-likes')[:5]
    context = {'categories': qs}
    return HttpResponse(render(request, 'rango/index.html', context))


def about(request):
    return HttpResponse(render(request, 'rango/about.html'))


def category(request, category_id):
    # add visits of category
    category = Category.objects.get(pk=category_id)
    if category:
        category.visits += 1
        category.save()
    pages = Page.objects.filter(category_id=category_id)
    return HttpResponse(render(request, 'rango/category.html', {'pages': pages}))
