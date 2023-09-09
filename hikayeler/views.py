import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import Hikayeler,HikayeAltKategori,FavoriHikayeler,BegeniHikayeler
from django.core.paginator import Paginator
from sairler.models import Sairler
from siirler.models import Siirler
from sozler.models import Sozler
from sozler.views import bunlarLazim
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count





def alt_kategori_detail(request, alt_kategori_slug):
    alt_kategori = get_object_or_404(HikayeAltKategori, slug=alt_kategori_slug)
    Hikaye = Hikayeler.objects.filter(alt_kategorisi=alt_kategori).order_by('?')
    sayfa_adi = f"En Güzel {alt_kategori.alt_kategori_adi}"

    paginator = Paginator(Hikaye, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Hikayeler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Hikayeler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = HikayeAltKategori.objects.filter(banner=True)
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]


    if page_number is None:
        page_number = 1
    context = {
        'icerik': icerik,
        'alt_kategori': alt_kategori,
        'sayfa_adi': sayfa_adi,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': alt_kategori.alt_kategori_adi,
        'description': f"{alt_kategori.meta_description} - Sayfa {page_number}",
        'keywords': alt_kategori.keywords,
    }
    return render(request, 'system/hikaye/hikaye_coklu_sayfa.html', context)


def hikaye_home(request):
    tum_banner_alt_kategoriler = HikayeAltKategori.objects.filter(banner=True)
    hikayePopuler = Hikayeler.objects.filter(small_banner=True)[:15]
    CokOkunanHikayeler = Hikayeler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]
    son_eklenen_Hikayeler = Hikayeler.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:8]
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    CokBeginiAlan = Hikayeler.objects.annotate(begeni_sayisi=Count('begenihikayeler')).order_by('-begeni_sayisi')[:15]

    title = "En Güzel Hikayeler"
    description = "Aradığınız her konuya ait aşk, sevgi, dini, atatürk, vatan hikayelerimizi okuyabilir dilerseniz kendi hikayelerinizi paylaşabilirsiniz."
    keywords = "dini hikayeler, ilginç hikayeler, aşk hikayeleri, cocuk hikayeleri, ibretlik hikayeler, etkileyici hikayeler, komik hikayeler"

    context = {
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,#popülerKategoriler
        'populersiir': hikayePopuler,
        'CokOkunanSiirler': CokOkunanHikayeler,
        'son_eklenen_siirler': son_eklenen_Hikayeler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'CokBeginiAlan': CokBeginiAlan,
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/hikaye/hikaye_home.html', context)




def hikaye_detail(request, hikaye_slug):
    siir = get_object_or_404(Hikayeler, slug=hikaye_slug)
    siir.okundu()


    tum_banner_alt_kategoriler = HikayeAltKategori.objects.filter(banner=True)
    random_Soz = Sozler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?').first()
    siirRandomsag, sairRandomsag, sozRandom, siirRandom, yazarRandom, hikayeRandom = bunlarLazim(siir)

    quotes = [
        "Sözlerin gücü, insanların kalplerini fetheden ve dünyayı değiştiren güzellikte gizlidir.",
        "Sözlerin büyüsü, geçmiş ve şimdiki zamanın öncülerinin unutulmaz alıntılarında gizlidir.",
        "Sözlerin dokunuşu, kalplerde açan çiçekler gibi duyguları renklendirir ve ilham verir.",
        "Sözlerin büyüsü, insanların kalbinde sonsuz bir iz bırakacak kadar etkileyicidir."
    ]

    sozbasligi = random.choice(quotes)

    context = {
        'siir': siir,
        'sozbasligi': sozbasligi,
        'random_Soz': random_Soz,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,  # popülerKategoriler
        'sozRandom': sozRandom,
        'siirRandom': siirRandom,
        'yazarRandom': yazarRandom,
        'hikayeRandom': hikayeRandom,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
    }
    return render(request, 'system/hikaye/hikaye_detail.html', context)




@login_required
def favori(request, siir_id):
    siir = get_object_or_404(Sozler, id=siir_id)
    FavoriHikayeler.objects.get_or_create(soz=siir, kullanici=request.user)
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)
@login_required
def favori_kaldir(request, siir_id):
    siir = get_object_or_404(Sozler, id=siir_id)
    FavoriHikayeler.objects.filter(soz=siir, kullanici=request.user).delete()
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)



@login_required
def begen(request, siir_id):
    siir = get_object_or_404(Hikayeler, id=siir_id)
    BegeniHikayeler.objects.get_or_create(hikayeler=siir, kullanici=request.user)
    return redirect('hikaye:hikaye_slug',  hikaye_slug=siir.slug)
@login_required
def begen_kaldir(request, siir_id):
    siir = get_object_or_404(Sozler, id=siir_id)
    BegeniHikayeler.objects.filter(soz=siir, kullanici=request.user).delete()
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)




def coklu_sayfa(request):
    url_name = request.resolver_match.url_name

    if url_name == 'populer-hikayeler':
        siir = Hikayeler.objects.filter(small_banner=True,status="Yayinda",aktif=True).order_by('?')
        sayfa_adi = "Popüler Hikayeler"
        title = "Popüler Hikayeler"
        description = "Popüler olan hikayeleri okuyabilir sevdiklerinizle paylaşabilir dilerseniz kendinizde hikayeler yazabilirsiniz."
        keywords = "güzel hikayeler, kısa hikayeler, aşk hikayeleri, cocuk hikayeleri, ibretlik hikayeler, etkileyici hikayeler, komik hikayeler"
    elif url_name == 'cok-okunan-hikaye':
        siir = Hikayeler.objects.filter(small_banner=True,status="Yayinda",aktif=True).order_by('-okunma_sayisi')
        sayfa_adi = "En Çok Okunan Hikayeler"
        title = "En Çok Okunan Hikayeler"
        description = "En çok okunan hikayeler takip edebilir dilerseniz bu zevkli maratona sizlerde hikayelerinizi paylaşıp katılabilirsiniz."
        keywords = "dini hikayeler, ilginç hikayeler, aşk hikayeleri, cocuk hikayeleri, uzun hikayeler, etkileyici hikayeler, komik hikayeler"
    elif url_name == 'en-son-eklenen-hikaye':
        siir = Hikayeler.objects.filter(status="Yayinda",aktif=True).order_by('-olusturma_tarihi')
        sayfa_adi = "En Son Eklenen Hikayeler"
        title = "En Son Eklnen Hikayeler"
        description = "En son eklenen hikayeleri buradan takip edebilirsiniz dilerseniz kendi hikayelerinizi paylaşabilirsiniz."
        keywords = "dini hikayeler, ilginç hikayeler, aşk hikayeleri, cocuk hikayeleri, ibretlik hikayeler, etkileyici hikayeler, komik hikayeler"
    elif url_name == 'cok-begeni-alan-hikayeler':
        siir = Hikayeler.objects.filter(status="Yayinda",aktif=True).annotate(begeni_sayisi=Count('begenihikayeler')).order_by('-begeni_sayisi')
        sayfa_adi = "En Çok Beğeni Alan Hikayeler"
        title = "En Çok Beğeni Alan Hikayeler"
        description = "Kullanıcılar tarafından en çok beğeni alan hikayeler dilerseniz kendi hikayelerinizi paylaşabilir sizde bu heyecanı yaşıyabilirsiniz."
        keywords = "dini hikayeler, romantik aşk hikayeler, aşk hikayeleri, gerçek hikayeler, ibretlik hikayeler, etkileyici hikayeler, meşhur aşk hikayeleri"



    paginator = Paginator(siir, 10) # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = HikayeAltKategori.objects.filter(aktif=True,banner=True)
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    if page_number is None:
        page_number = 1
    description = f"{description} - Sayfa {page_number}"

    context = {
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,

        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/hikaye/hikaye_coklu_sayfa.html', context)


def all_Kategori(request):
    tum_alt_kategoriler = HikayeAltKategori.objects.all()
    cok_okunan_Hikaye = Hikayeler.objects.filter(small_banner=True,status="Yayinda",aktif=True).order_by('-okunma_sayisi')[:8]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = HikayeAltKategori.objects.filter(aktif=True, banner=True)
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    title = "Tüm Hikaye Kategorileri, Aşk Hikayeleri"
    description = "Tüm hikayelerin konu başlıkları, aşk hikayeleri, dini hikayeler ve çok daha fazla hikaye kategorisi, hadi sizde hikayelerinizi bizimle paylaşın"
    keywords = "dini hikayeler, romantik aşk hikayeler, kısa hikayeler, uzun hikayeler, aşk hikayeleri, gerçek hikayeler, ibretlik hikayeler, etkileyici hikayeler, meşhur aşk hikayeleri"


    context = {
        'tum_alt_kategoriler': tum_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': cok_okunan_Hikaye,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/hikaye/tum_hikaye_kategori.html', context)