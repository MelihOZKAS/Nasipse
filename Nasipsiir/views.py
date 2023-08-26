from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect
from siirler.models import *
from sairler.models import Sairler
from sozler.models import Sozler
from userPanel.form import KayitOlFormu,LoginForm
from userPanel.models import CustomUserManager
from django.views.decorators.http import require_GET
import requests
import random
from django import forms
from itertools import chain
from random import shuffle
from django.contrib.auth import authenticate, login,logout

from userPanel.models import CustomUserManager,CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


def home(request):
    keyler = AnasayfaKeyler.objects.first()

    son_eklenen_siirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:10]
    Banner = Siirler.objects.filter(aktif=True, status="Yayinda", banner=True).order_by('?')[:3]
    Small_Banner = Siirler.objects.filter(aktif=True, status="Yayinda", small_banner=True).order_by('?')[:3]

    Sair_Banner = Sairler.objects.filter(aktif=True, status="Yayinda", banner=True).order_by('?')[:3]
    Populer_sair = Sairler.objects.filter(aktif=True, status="Yayinda", small_banner=True).order_by('?')[:9]

    Populer_Sozler = Sozler.objects.filter(aktif=True, status="Yayinda", small_banner=True).order_by('?')[:9]
    Banner_Soz = Sozler.objects.filter(aktif=True, status="Yayinda", small_banner=True).order_by('?')[:10]
    son_eklenen_Sozler = Sozler.objects.filter(aktif=True, status="Yayinda", small_banner=True).order_by('-olusturma_tarihi')[:10]



    tum_bannerlar = list(chain(Banner, Sair_Banner))
    shuffle(tum_bannerlar)

    context = {
        "keyler": keyler,
        "Banner": tum_bannerlar,
        "Small_Banner": Small_Banner,
        "son_eklenen_siirler": son_eklenen_siirler,
        "Populer_sair": Populer_sair,
        "Populer_Sozler": Populer_Sozler,
        "Banner_Soz": Banner_Soz,
        "son_eklenen_Sozler": son_eklenen_Sozler,
    }



    return render(request, 'system/home.html', context)


def kayitol(request):
    if request.method == 'POST':
        form = KayitOlFormu(request.POST)
        if form.is_valid():
            # Form verilerini session'a kaydet
            request.session['form_data'] = form.cleaned_data

            # Doğrulama kodunu oluştur
            verification_code = random.randint(100000, 999999)

            # Doğrulama kodunu SMS ile gönder
            phone_number = form.cleaned_data['phone_number']
            response = requests.get(
                'https://api.netgsm.com.tr/sms/send/get',
                params={
                    'usercode': '8503033935',
                    'password': 'Melih4466.',
                    'gsmno': phone_number,
                    'message': f'{verification_code} kodunu girerek telefon numaranızı doğrulayın',
                    'msgheader': '8503033935'
                }
            )

            # Doğrulama kodunu session'a kaydet
            request.session['verification_code'] = verification_code

            # Kullanıcıyı doğrulama sayfasına yönlendir
            return redirect('sms-kontrol')
        else:
            print(form.errors)

    return render(request, 'system/user/kayit-ol.html')



def SMSKontrol(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if int(code) == request.session.get('verification_code'):
            # Doğrulama başarılı
            # Form verilerini session'dan al
            form_data = request.session.get('form_data')

            print(form_data['username'],form_data['first_name'],form_data['last_name'],form_data['email'],form_data['phone_number'],form_data['password1'])

            user = CustomUser.objects.create_user(

                username=form_data['username'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                email=form_data['email'],
                phone_number=form_data['phone_number'],
                password=form_data['password1'],
                hakkinda_ozet=f"BilgiBekleniyor",
                hakkinda_detay="Bilgibekleniyor"
            )

            # Ana sayfaya yönlendir
            return redirect('giris-yap')
        else:
            print(code)
            print(request.session.get('verification_code'))

            print(type(code))
            print(type(request.session.get('verification_code')))

            print("HataliSifre")
            # Doğrulama başarısız
            # Hata mesajı göster ve doğrulama formunu tekrar göster
          #  messages.error(request, 'Doğrulama kodu yanlış. Lütfen tekrar deneyin.')

    return render(request, 'system/user/SMSKontrol.html')



def cikis(request):
    logout(request)

    return redirect('home')
@require_GET
def robots_txt(request):
    content = "User-agent: *\nAllow: /"
    content = content.decode("latin-1")
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def girisyap1(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("Basarili")
                # Giriş başarılı
                # Ana sayfaya yönlendir
                return redirect('konsol:home')
            else:
                print("Hatali Şifre")
                # Giriş başarısız
                # Hata mesajı göster
                #messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
        else:
            print(form.errors)



    return render(request, 'system/user/giris-yap.html')





def girisyap(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

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

            # Kullanıcı doğrulandı, giriş yap
            user = authenticate(request, username=user, password=password)
            if user is not None:
                login(request, user)
                print("Basarili")
                # Giriş başarılı
                # Ana sayfaya yönlendir
                return redirect('konsol:home')
            else:
                print("Hatali Şifre")
                # Giriş başarısız
                # Hata mesajı göster
                #messages.error(request, 'Kullanıcı adı veya şifre yanlış.')



    return render(request, 'system/user/giris-yap.html')


