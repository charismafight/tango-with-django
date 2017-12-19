from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CategoryForm, PageForm, UserProfileForm, UserForm
from .models import *


# Create your views here.
def index(request):
    # request.session.set_test_cookie()
    qs = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context = {'categories': qs, 'pages': pages}

    visits = int(request.COOKIES.get('visits', 1))
    reset_last_visit_time = False

    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    context['visits'] = visits
    response = render(request, 'rango/index.html', context)
    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)
    return response


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
    # if request.session.test_cookie_worked():
    #     print('cookie worked')
    # else:
    #     print('cookie does not worked')
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            # set password by set_password func cause it's a hash func
            user.set_password(user.password)
            user.save()

            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user

            # dealing with the picture file
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            user_profile.save()

            registered = True
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    # when a new or modify page was setup,we should consider both post(submit page) and get(init page)
    # generally speaking,the keys of the context for the page may be the same when post and get
    # just different in content
    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        userpwd = request.POST.get('userpwd')

        user = authenticate(username=username, password=userpwd)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
        else:
            print('error username or password,please try again')
            return HttpResponse('error username or password,please try again')
    else:
        return render(request, 'rango/login.html')


@login_required
def restrict(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
