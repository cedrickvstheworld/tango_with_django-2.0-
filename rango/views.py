from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import Page, Category, UserProfile, Like
from . forms import CategoryForm, PageForm, UserForm, UserProfileForm


# Create your views here.
def decen(x):
    if x.find(' ') != -1:
        a = x.replace(' ', '_')
        return a
    elif x.find('_') != -1:
        a = x.replace('_', ' ')
        return a
    else:
        return x


def category_lists():
    categories = Category.objects.order_by('-likes')

    for i in categories:
        i.url = decen(i.name)

    return categories


@login_required
def category_like(request):
    if request.method == 'POST':
        category_id = request.POST['category_id']

        category = Category.objects.get(id=int(category_id))

        if request.POST['fuckingaction'] == 'likethisshit':
            try:
                Like.objects.get(user=request.user, category=category, liked=True)
            except:
                category.likes += 1
                category.save()

                Like.objects.create(
                    liked = True,
                    category = category,
                    user = request.user,
                )
        else:
            category.likes -= 1
            category.save()
            Like.objects.filter(user=request.user, category=category, liked=True).delete()

    return HttpResponse('')


def track_url(request):
    url = ''
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)


def search(request):
    search_text = ''
    category = ''
    if request.method == 'POST':
        search_text = request.POST['search_text']
        category = request.POST['category']
    categoryname = Category.objects.get(name=category)
    pages = Page.objects.filter(category=categoryname).filter(title__icontains=search_text)

    return render_to_response('rango/pagesearch.html', {'pages': pages})


def categorysearch(request):
    search_text = ''
    if request.method == 'POST':
        search_text = request.POST['search_text']
    categoryx = Category.objects.filter(name__icontains=search_text)

    for i in categoryx:
        i.url = decen(i.name)

    return render_to_response('rango/categorysearch.html', {'cat_list': categoryx})



def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': categories,
        'pages': pages,
        'cat_list': category_lists()
    }
    for i in categories:
        i.url = decen(i.name)

    return render(request, 'rango/index.html', context_dict)



def category(request, category_name_url):
    category_name = decen(category_name_url)
    context_dict = {
        'category_name': category_name,
        'category_name_url': category_name_url,
        'cat_list': category_lists()
    }

    try:

        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['category'] = category
        context_dict['pages'] = pages
        
        if request.user.is_authenticated:
            liked = Like.objects.get(
                user=request.user,
                category=category
            )

            context_dict['liked'] = liked

    except Like.DoesNotExist:
        pass

    except Category.DoesNotExist:
        pass


    return render(request, 'rango/category.html', context_dict)



def seachincategory(category_name, key):
    category = Category.objects.get(name=category_name)
    search_result = Page.objects.filter(category=category)
    filtered_page = []

    for i in search_result:
        if i.title.lower().find(key.lower()) != -1:
            filtered_page.append(i)

    return filtered_page


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context_dict = {
        'form': form,
        'cat_list': category_lists()
    }
    return render(request, 'rango/add_category.html', context_dict)

@login_required
def add_pages(request, category_name_url):
    category_name = decen(category_name_url)
    form = PageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            page = form.save(commit=False)
            cat = Category.objects.get(name=category_name)
            page.category = cat
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()
    context_dict = {
        'form': form,
        'category_name': category_name,
        'category_name_url': category_name_url,
        'cat_list': category_lists()
    }
    return render(request, 'rango/add_pages.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'cat_list': category_lists()
    }

    return render(request, 'rango/register.html', context_dict)


@login_required
def profile(request):
    user_datax = UserProfile()
    user_data = user_datax.fetchuserprofile(request.user)

    context_dict = {
        'user': user_data[0],
        'user_profile': user_data[1],
        'cat_list': category_lists()
    }

    return render(request, 'rango/profile.html', context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user=user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'rango/login.html', {'error': 'incorrect username or password'})
    elif request.COOKIES.get('sessionid'):
        return HttpResponseRedirect('/')
    else:
        return render(request, 'rango/login.html',
                      {'cat_list': category_lists()}
                      )


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
