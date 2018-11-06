from django.contrib import auth as django_auth
import base64
from django.http import JsonResponse
from sign.models import Event
from sign.models import Guest
import time
from hashlib import md5
from django.core.exceptions import ValidationError,ObjectDoesNotExist


# 用户签名+时间戳
def user_sign(request):
    if request.method=='POST':
        client_time=request.POST.get('time','')
        client_sign=request.POST.get('sign','')
    else:
        return "error"
    if client_time == '' or client_sign=='':
        return "sign null"

    # 服务器时间
    now_time = time.time()
    server_time=str(now_time).split(".")[0]
    # 获取时间
    time_difference = int(server_time) - int(client_time)
    if time_difference >=60:
        return "timeout"

    #签名检查
    sign_str = client_time + "&Guest-Bugmaster"
    sign_byte_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_byte_utf8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return "sign fail"
    else:
        return "sign success"

#用户认证
def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION',b'')
    auth = get_http_auth.split()
    print(auth)
    try:
        # partition 可按指定的字符分割字符串
        auth_paths = base64.b64decode(auth[1]).decode('utf-8').partition(':')
        # base64编码/解码均要求 对象类型为bytes 不能为str 字符串型  如果是字符串类型 需要先转换为byte型
        # 例 s='this a test text'
        #sb=s.encode（'utf-8'）
        #s64=base64.b64decode(sb)
       # print(auth_paths)
    except IndexError:
        return "null"
    username,password = auth_paths[0],auth_paths[2]
    user = django_auth.authenticate(username=username,password=password)
    print(user)
    if user is not None:
        django_auth.login(request,user)
        return "success"
    else :
        return "fail"

# 用户签名方式+添加发布会接口
def add_event(request):
    sign_result = user_sign(request)
    if sign_result == "error":
        return JsonResponse({"status":10011,'message':'request error'})
    elif sign_result == "sign null":
        return JsonResponse({"status":10012,'message':'user sign null'})
    elif sign_result == "sign fail":
        return JsonResponse({"status":10014,'message':'user sign timeout'})
    elif sign_result == "timeout":
        return JsonResponse({"status":10013,'message':'user sign timeout'})
    # 添加发布会
    if sign_result == "sign success":
        eid = request.POST.get('eid', '')  # 发布会id
        name = request.POST.get('name', '')  # 发布会标题
        limit = request.POST.get('limit', '')  # 限制人数
        status = request.POST.get('status', '')  # 状态
        address = request.POST.get('address', '')  # 地址
        start_time = request.POST.get('start_time', '')  # 发布会时间
        #print(eid, name)
        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        result = Event.objects.filter(id=eid)
        if result:
            return JsonResponse({'status': 10022, 'message': 'event id already exists'})
        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({'status': 10023, 'message': 'event name already exists'})
        if status == 'True':
            status = 1
        elif status == 'False':
            status = 0

        if status == '':
            status = 1

        try:
            Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status),
                                 start_time=start_time)
        except ValidationError as e:
            error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
            return JsonResponse({'status': 10024, 'message': error})

        return JsonResponse({'status': 200, 'message': 'add event success'})




#查询发布会+安全用户认证
def get_event_list(request):
    auth_result = user_auth(request)
    if auth_result=="null":
        return JsonResponse({'status':10011,'message':'user auth null'})
    if auth_result=="fail":
        return JsonResponse({'status':10012,'message':'user auth fail'})

    eid= request.GET.get("eid",'')
    name = request.GET.get("name",'')
    if eid=='' and name=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':'10022','message':'query result is empty'})
        else:
             event['name'] = result.name
             event['limit'] = result.limit
             event['status'] = result.status
             event['address'] = result.address
             event['start_time'] = result.start_time
             return JsonResponse({'status':200,'message':'success','data':event})

    if name != '':
        datas=[]
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','datas':datas})
        else:
            return JsonResponse({'status':10022,'message':'query result is empty'})