# _author: 17393
# date: 2020/7/17
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from web import models
from web.forms.bootstrap import BootstrapForm


class RegisterModelForm(BootstrapForm, forms.ModelForm):
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(),
                               min_length=6,
                               max_length=18,
                               error_messages={
                                   'min_length': '密码长度至少为6位',
                                   'max_length': '密码长度不得少于18位'
                               }
                               )
    confirm_password = forms.CharField(label="重复密码",
                                       min_length=6,
                                       max_length=18,
                                       error_messages={
                                           'min_length': "密码长度不能少于6位",
                                           'max_length': "密码长度不能多于18位"
                                       },
                                       widget=forms.PasswordInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'mobile_phone', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).first()

        if exists:
            raise ValidationError("用户名已经存在，请重新输入！")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).first()
        if exists:
            raise ValidationError("邮箱已被注册，请重新输入！")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已经被注册")

        return mobile_phone

    def clean_password(self):

        password = self.cleaned_data['password']

        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        # confirm_password = self.cleaned_data['confirm_password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError("两次输入密码不一致")

        return confirm_password


class LoginForm(BootstrapForm, forms.Form):
    username = forms.CharField(label="手机号或邮箱")
    # render_value = True  保证页面刷新，保留上次输入的密码
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label="图片验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        password = self.cleaned_data['password']

        return password

    def clean_code(self):
        code = self.cleaned_data['code']

        # 去session获取自己code
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError("验证码已过期，请重新获取！")
        if session_code.strip().upper() != code.strip().upper():
            raise ValidationError("验证码错误，请重新输入！")

        return code
