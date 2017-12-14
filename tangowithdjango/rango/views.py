from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CategoryForm, PageForm, UserProfileForm, UserForm
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
    current_category = Category.objects.get(slug=category_name)
    if current_category:
        current_category.visits += 1
        current_category.save()
    pages = Page.objects.filter(category=current_category)
    return HttpResponse(
        render(request, 'rango/category.html', {'pages': pages, 'category': current_category}))


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


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form and form.is_valid():
            if cat:
                # form has no category attribute,so it needs to save twice here
                # this is the form's save
                page = form.save(commit=False)
                page.category = cat
                # and this is the model's
                page.save()
                # return the view when saved successful

                # we can also call the category func here instead of using redirect and reverse
                return category(request, category_name_slug)
                # return HttpResponseRedirect(reversed('category', args=(category_name_slug,)))
        else:
            print(form.errors)
    else:
        form = PageForm()
    context = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context)


def regiter(request):
    registered = False
    if request.method == 'POST':
        pass
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
        context = {'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered}
        return render(request, 'rango/register.html', context)
