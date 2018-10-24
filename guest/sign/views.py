from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  #引入django自带分页器模块
# Create your views here.
def index(request):
    #return HttpResponse("Hello Django!")
    return render(request,"index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        #if username == 'admin' and password == 'admin123' :
        if user is not None:
            #return HttpResponse('login success!')
            auth.login(request,user)         # 登录
            response = HttpResponseRedirect('/event_manage/')
           #response.set_cookie('user',username, 3600)  存储浏览器cookie 存放时长3600 秒
            request.session['user'] = username # 将session信息记录到浏览器
            return response
        else :
            return  render(request,'index.html',{'error':'username or password error' })

@login_required # django 装饰器登录认证 防止跨站访问
def event_manage(request):
    #username = request.COOKIES.get('user', '') #读取浏览器cookie
    username = request.session.get('user','') #读取浏览器session
    event_list = Event.objects.all()
    return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def sign_manage(request,eid):
    #username = request.sessions.get('user','')
    limit = Event.objects.get(id=eid).limit  # 获取发布会限制人数
    current_num = Guest.objects.filter(sign=True, event_id=eid).__len__()  # 当前已签到人数
    event = get_object_or_404(Event, id=eid)
    return render(request,'sign_index.html',{'event':event,'limit':limit,'sign_num':current_num})

@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone','')
    print(phone)
    limit = Event.objects.get(id=eid).limit # 获取发布会限制人数
    current_num=Guest.objects.filter(sign=True,event_id=eid).__len__()# 当前已签到人数
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error'})
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        current_num = Guest.objects.filter(sign=True, event_id=eid).__len__()
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result,'limit':limit,'sign_num':current_num})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list =  Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try :
        contracts = paginator.page(page)
    except PageNotAnInteger:
        #  如果page不是整数，取第一页数据
        contracts = paginator.page(1)
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contracts})




@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')# 搜索框form中定义方法get 及input name
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})



@login_required
def search_person(request):
    username = request.session.get('user','')
    search_person = request.GET.get('realname','')
    guest_list = Guest.objects.filter(realname__contains = search_person)
    #return render(request,"guest_manage.html",{"user":username,"guests":guest_list})
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try :
        contracts = paginator.page(page)
    except PageNotAnInteger:
        #  如果page不是整数，取第一页数据
        contracts = paginator.page(1)
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contracts})

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response