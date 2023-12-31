from django.shortcuts import render,redirect,get_object_or_404
from .models import Sairler,FavoriSair,BegeniSair
from siirler.models import Siirler,SiirAltKategori
from sozler.models import Sozler
from sozler.views import bunlarLazim
import random
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

def sair_home_detail(request, ):
    populersiir = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True)[:15]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]
    son_eklenen_Yazarlar = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:8]
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairpopuler = Sairler.objects.filter(aktif=True, small_banner=True, status="Yayinda").order_by('?')[:15]
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,siir=True)
    tum_banner_alt_kategoriler_soz = SiirAltKategori.objects.filter(banner=True,soz=True)

    title = "Türk Edebiyatı'nın En Ünlü Şairleri Eserleri ve Biyografileri"
    description = "Şairlerimizin eserleri ve biyografilerine ulaşabilirsiniz. Ünlü şairlerimizin şiirlerini ve hayat hikayelerini keşfedebilir, en büyük şairlerin eserlerine buradan ulaşabilirsiniz."
    keywords = "şiir, şair, en ünlü şairler, türk edebiyatı, şair biyografileri, türk ünlü şairler, türk şairler, kadın şairler"

    context = {
        'CokOkunanSiirler': CokOkunanSiirler,
        'son_eklenen_Yazarlar': son_eklenen_Yazarlar,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'sairpopuler': sairpopuler,
        'tum_banner_alt_kategoriler': tum_banner_alt_kategoriler,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'tum_banner_alt_kategoriler_soz': tum_banner_alt_kategoriler_soz,
        'populersiir': populersiir,
        'title' : title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/sair/sair_home.html', context)



def sair_detail(request,  sair_slug):
    sair = get_object_or_404(Sairler, slug=sair_slug)
    sair.okundu()
    siir = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?').first()
    random_Soz = Sozler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?').first()

    if not isinstance(request.user, AnonymousUser):
        favoride = FavoriSair.objects.filter(sair=sair, kullanici=request.user).exists()
        begenildi = BegeniSair.objects.filter(sair=sair, kullanici=request.user).exists()
    else:
        favoride = False
        begenildi = False


    siirRandomsag, sairRandomsag, sozRandom, siirRandom, yazarRandom, hikayeRandom = bunlarLazim(siir)
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, soz=True)

    quotes = [
        "Sözlerin gücü, insanların kalplerini fetheden ve dünyayı değiştiren güzellikte gizlidir.",
        "Sözlerin büyüsü, geçmiş ve şimdiki zamanın öncülerinin unutulmaz alıntılarında gizlidir.",
        "Sözlerin dokunuşu, kalplerde açan çiçekler gibi duyguları renklendirir ve ilham verir.",
        "Sözlerin büyüsü, insanların kalbinde sonsuz bir iz bırakacak kadar etkileyicidir."
    ]

    sozbasligi = random.choice(quotes)

    context = {
        'sair': sair,
        'Siirler': siir,
        'favoride': favoride,
        'begenildi': begenildi,
        'sozbasligi': sozbasligi,
        'random_Soz': random_Soz,
        'sozRandom': sozRandom,
        'siirRandom': siirRandom,
        'yazarRandom': yazarRandom,
        'hikayeRandom': hikayeRandom,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
    }
    return render(request, 'system/sair/sair_detail.html', context)

def populer_sair_detail(request):
    sairler = Sairler.objects.filter(aktif=True,status="Yayinda",small_banner=True)
    paginator = Paginator(sairler, 12)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    if page_number is None:
        page_number = ""
    title = f"Popüler Şairler - {page_number}"
    description = f"Popüler şairlerimizin ve yazarlarımızın listesi aradığınız tüm şair ve yazarların özet bilgileri ve tüm bilgileri yer almaktadır - Sayfa {page_number}"
    keywords = "en sevilen şairler, en çok okunan yazarlar, sevilen yazarlar, popüler yazarlar, şairler, yazarlar"


    context = {
        'icerik': icerik,
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/sair/sair_listesi.html', context)


@login_required
def favori(request, siir_id):
    siir = get_object_or_404(Sairler, id=siir_id)
    FavoriSair.objects.get_or_create(sair=siir, kullanici=request.user)
    return redirect('sairler:sair_detail', sair_slug=siir.slug)
@login_required
def favori_kaldir(request, siir_id):
    siir = get_object_or_404(Sairler, id=siir_id)
    FavoriSair.objects.filter(sair=siir, kullanici=request.user).delete()
    return redirect('sairler:sair_detail', sair_slug=siir.slug)



@login_required
def begen(request, siir_id):
    siir = get_object_or_404(Sairler, id=siir_id)
    BegeniSair.objects.get_or_create(sair=siir, kullanici=request.user)
    return redirect('sairler:sair_detail', sair_slug=siir.slug)
@login_required
def begen_kaldir(request, siir_id):
    siir = get_object_or_404(Sairler, id=siir_id)
    BegeniSair.objects.filter(sair=siir, kullanici=request.user).delete()
    return redirect('sairler:sair_detail', sair_slug=siir.slug)
