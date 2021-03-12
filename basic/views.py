from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def setting(request):
    if request.method=='POST':
        s= request.POST['your_name']
        request.session['refvar']=s

        return HttpResponse('session name is set')
    if request.method=='GET':
        return render(request,'index.html')


# session stores in db
def checking(request):

    if request.method=='POST':
        ourvalue = request.POST['your_name']

        print('our value is',ourvalue)
        try:
            if ourvalue in request.session.get('refvar'):
                st="<h2>name is present"+request.session.get('refvar'),"</h2>"
                return HttpResponse(st)
            else:
                kt="<h2>name is not present",request.session.get('refvar','universal user'),"</h2>"
                return HttpResponse(kt)
        except:
            return HttpResponse("its already deleted")



    if request.method=='GET':

        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        context = {

            'num_visits': num_visits,
        }
        return render(request,'index.html',context=context)


def delete_session(request):
    if request.method=='POST':
        val1 = request.POST['your_name']
        if val1 in request.session['refvar']:
            del request.session['refvar']
            return HttpResponse("the value has been deleted")

        else:
            return HttpResponse("value is not present in session to delete")
    if request.method=='GET':
        return render(request,'index.html')


def set_coockie(request):
    if request.method=='POST':
        cookieid=request.POST['your_key']
        cookiename = request.POST['your_name']
        st = HttpResponse(" Testing the cookies ")
        st.set_cookie(cookieid,cookiename,max_age=500)
        return st
    if request.method=='GET':
        return render(request, 'index.html')


def show_cookie(request):
    if request.method=='POST':
        n = request.POST['your_name']
        cookieid = request.POST['your_key']
        show  =  request.COOKIES[cookieid]
        if n == show:
            return HttpResponse("the value in the cookie is "+show)
        else:
            return HttpResponse("the entered value is not matching with value in cookie")

    if request.method=='GET':
        return render(request,'index.html')



def delete_cookie(request):
    if request.method=='POST':
        cookiedata = request.POST['your_name']
        cookieid = request.POST['your_key']
        delete = request.COOKIES[cookieid]

        if cookiedata== delete:
            st = HttpResponse("the value is getting deleted")
            st.delete_cookie(cookieid)
            return st

        else:
            return HttpResponse("the value does not match with the vlaue in cookie ")

    if request.method=='GET':
        return render(request,'index.html')

from django.views.decorators.cache import cache_page
from datetime import datetime

@cache_page(10)
def hello(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return HttpResponse(current_time)

@cache_page(8)

def hi(requets):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return HttpResponse(current_time)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def locations(request):
    user_list= Location.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user_list.html', { 'users': users })
