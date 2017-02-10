from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.http import HttpResponse
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm
from rango.forms import UserProfileForm

def index(request):
    categoty_list = Category.objects.order_by('-likes')[:5] #creating list of 5 most liked categories
    page_list = Page.objects.order_by('-views')[:5]         #creating list of 5 most viewed pages
    context_dict = {'categories':categoty_list,'pages':page_list}       #
    return render(request,'rango/index.html',context=context_dict)      #passes lists for use on server

def about(request):     #about page and its string message
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>index<a/>")

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['pages'] = none
        context_dict['category'] = none
    return render(request,'rango/category.html',context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html',{'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    form = PageForm()
    if request.method=='POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict = {'forms':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)

def register(request):
    registered = False
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfilerForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save

            registered=true
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

