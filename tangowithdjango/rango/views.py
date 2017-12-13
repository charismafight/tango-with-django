from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse

from .forms import CategoryForm
from .models import *


# Create your views here.
def index(request):
    qs = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context = {'categories': qs, 'pages': pages}
    return HttpResponse(render(request, 'rango/index.html', context))


def about(request):
    return HttpResponse(render(request, 'rango/about.html'))


def category(request, category_name):
    # add visits of category
    current_category = get_object_or_404(Category, slug=category_name)
    if current_category:
        current_category.visits += 1
        current_category.save()
    pages = get_list_or_404(Page, category=current_category)
    return HttpResponse(
        render(request, 'rango/category.html', {'pages': pages, 'category_name': current_category.name}))


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})
