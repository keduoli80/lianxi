import json
import random

from django.shortcuts import render ,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

from web.forms.account import RegisterModelForm,SendSmsForm,Login

from utils.send_email import send_register_email
from web import models
from django_redis import get_redis_connection
from utils.send_email import code_yan

@csrf_exempt
def register(request):
    if request.method=='GET':
        form=RegisterModelForm()
        return render(request,'register.html',{'form':form})
    form=RegisterModelForm(data=request.POST)
    if form.is_valid():
        email=form.cleaned_data.get('email')
        user_email=models.UserInfo.objects.filter(email=email).first()
        request.session['user_id']=user_email.id
        request.session['user_name'] = user_email.username
        form.save()
        return HttpResponse(json.dumps({'status':True,'data':'/web/login/'}))
    return HttpResponse(json.dumps({'status':False,'error':form.errors}))



@csrf_exempt
def send_sms(request):
    ject_code = code_yan()
    form=SendSmsForm(data=request.POST)
    email= request.POST.get('email')
    if form.is_valid():
        conn = get_redis_connection()
        conn.set(email, ject_code, ex=60)
        send_register_email(email,ject_code)
        return HttpResponse(json.dumps({'status':True}))
    return HttpResponse(json.dumps({'status':False,'error':form.errors}))

def login(request):
    if request.method=='GET':
        form=Login(request)
        return render(request,'login.html',{'form':form})
    form=Login(request,data=request.POST)
    if form.is_valid():
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        from django.db.models import Q
        user=models.UserInfo.objects.filter(Q(username=username)|Q(email=username)).filter(password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session.set_expiry(60*60*24*14)
            return redirect('/web/home')
        form.add_error('username','用户名或密码错误')
    return render(request, 'login.html', {'form': form})

def image_code(request):
    from utils.code import check_code
    image,code =check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)

    from io import BytesIO
    stream= BytesIO()
    image.save(stream,'png')
    return HttpResponse(stream.getvalue())

def login_out(request):
    request.session.flush()
    return redirect('/web/home')