from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from userPanel.models import CustomUserManager,CustomUser


class KayitOlFormu(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Zorunlu.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Zorunlu.')
    email = forms.EmailField(max_length=254, required=True, help_text='Zorunlu. Geçerli bir email adresi girin.')
    phone_number = forms.CharField(max_length=30, required=True, help_text='Zorunlu.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı veya E-posta')
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    print(username,password)

    def clean(self):
        super().clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        print(username)
        print(password)

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                raise forms.ValidationError('Kullanıcı bulunamadı.')

        if not user.check_password(password):
            raise forms.ValidationError('Şifre yanlış.')

        return self.cleaned_data

