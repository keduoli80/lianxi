from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection

from utils.md5 import md5
class RegisterModelForm(forms.ModelForm):
    password=forms.CharField(label='密码',
                             min_length=8,
                             max_length=16,
                             error_messages={'min_length':'密码长度小于8位',
                                             'max_length':'密码不能大于16位',
                                             },
                             widget=forms.PasswordInput())
    confirm_password=forms.CharField(label='重复密码',
                                     min_length=8,
                                     max_length=16,
                                     error_messages={'min_length': '密码长度小于8位',
                                                     'max_length': '密码不能大于16位',
                                                     },
                                     widget=forms.PasswordInput())
    code=forms.CharField(label='邮箱验证码',widget=forms.TextInput())
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput)

    class Meta:
        model=models.UserInfo
        fields=['username','email','password','confirm_password','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,value in self.fields.items():
            value.widget.attrs={'class':'form-control','placeholder':value.label}
            # value.widget.attrs['placeholder']='请输入%s'%(value.label,)也可以

    def clean_username(self):
        username=self.cleaned_data.get('username')
        exists=models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
            # self.add_error('username','用户名已存在')也可以不管通过不通过都执行下一步
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        exists=models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        con_pwd=self.cleaned_data.get('confirm_password')
        new_con_pwd=md5(con_pwd)
        if new_con_pwd!=pwd:
            raise ValidationError('前后密码不一致')
        return new_con_pwd

    def clean_code(self):
        email=self.cleaned_data.get('email')
        input_code=self.cleaned_data.get('code')
        if not email:
            return input_code

        conn=get_redis_connection()
        redis_code=conn.get(email)
        if not redis_code:
            raise ValidationError('验证码失效或未发送')
        str_redis=redis_code.decode('utf-8')
        if input_code.strip() != str_redis:
            raise ValidationError('验证码错误')
        return input_code






class SendSmsForm(forms.Form):
    email=forms.EmailField(label='邮箱',validators=[RegexValidator(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$','邮箱格式错误！')])
    def clean_mobile_phone(self):
        email=self.cleaned_data['email']
        exisit=models.UserInfo.objects.filter(email=email).exisit()
        if exisit:
            raise ValidationError('邮箱已存在')
        elif email=='':
            raise ValidationError('邮箱不能为空')
        return email


class Login(forms.Form):
    username=forms.CharField(label='用户名或邮箱')
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=16,
                               error_messages={'min_length': '密码长度小于8位',
                                               'max_length': '密码不能大于16位',
                                               },
                               widget=forms.PasswordInput(render_value=True))
    image_code = forms.CharField(label='验证码')

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
        for name,value in self.fields.items():
            value.widget.attrs={'class':'form-control','placeholder':value.label}

    def clean_image_code(self):
        code=self.cleaned_data['image_code']
        session_code=self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期')
        if code.strip().upper()!=session_code.strip().upper():
            raise ValidationError('验证码错误')
        return code
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)