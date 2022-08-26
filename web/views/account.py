from django.shortcuts import render ,HttpResponse,redirect

from web.forms.account import RegisterModelForm
def register(request):
    form=RegisterModelForm()
    return render(request,'register.html',{'form':form})