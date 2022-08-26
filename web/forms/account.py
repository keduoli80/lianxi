from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterModelForm(forms.ModelForm):
    mobile_phone=forms.CharField(label='手机号',validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9|])\d{9}$','手机号格式错误！'),])
    password=forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password=forms.CharField(label='重复密码',widget=forms.PasswordInput())
    code=forms.CharField(label='验证码',widget=forms.TextInput())
    class Meta:
        model=models.UserInfo
        fields=['username','email','password','confirm_password','mobile_phone','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,value in self.fields.items():
            value.widget.attrs={'class':'form-control','placeholder':value.label}
            # value.widget.attrs['placeholder']='请输入%s'%(value.label,)也可以