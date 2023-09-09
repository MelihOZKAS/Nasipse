from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from sairler.models import Sairler
from .models import Sozler,BegeniSozler,FavoriSozler,SiirAltKategori
from siirler.models import Siirler,SiirAltKategori
from django.core.paginator import Paginator
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser


# Create your views here.
def yazar_home_detail(request, ):
    populersiir = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True)[:15]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]
    son_eklenen_sozler = Sozler.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:8]
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairpopuler = Sairler.objects.filter(aktif=True, small_banner=True, status="Yayinda").order_by('?')[:15]
    tum_banner_alt_kategoriler_soz = SiirAltKategori.objects.filter(banner=True,soz=True)

    context = {

        'CokOkunanSiirler': CokOkunanSiirler,
        'son_eklenen_sozler': son_eklenen_sozler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'sairpopuler': sairpopuler,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler_soz,
        'populersiir': populersiir
    }
    return render(request, 'system/sozler/sozler_home.html', context)






def TumSozlerSade(request):
    url_name = request.resolver_match.url_name
    if url_name == "populer-guzel-sozler":
        siir = Sozler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('-olusturma_tarihi')
        title = "Popüler Güzel Sözler"
        description = "En güzel sözlerin paylaşıldığı hem şairlerin hem üyelerimizin kıymetli paylaşımları"
        keywords = "kısa sözler, özlü sözler, anlamlı sözler, cuma mesajı sözleri, baba sözler"
        sayfa_adi = "Popüler Güzel Sözler"
    elif url_name == "en-son-eklenen-guzel-sozler":
        siir = Sozler.objects.all().order_by('-olusturma_tarihi')
        title = "En Son Eklenen Güzel Sözler"
        description = "En son eklenen güzel sözler hem şair hem üyelerimizin en kıymetli paylaşımları"
        keywords = "anlamlı sözler, ilginç sözler, özlü sözler, güzel sözler, en güzel sözler"
        sayfa_adi = "En Son Eklenen Güzel Sözler"


    paginator = Paginator(siir, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, soz=True)
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]


    context = {
        'icerik': icerik,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,
        'sayfa_adi': sayfa_adi,
    }
    return render(request, 'system/sozler/soz_coklu_sayfa.html', context)




def all_Kategori(request):
    tum_alt_kategoriler = SiirAltKategori.objects.filter(aktif=True,soz=True)
    random_populer = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?')[:8]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, soz=True)
    siirRandomsag = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    context = {
        'tum_alt_kategoriler': tum_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,

        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,

    }
    return render(request, 'system/sozler/tum_soz_kategori.html', context)


def TumSozler(request,  sair_slug):
    BulunanSair = get_object_or_404(Sairler, slug=sair_slug)
    siir = Sozler.objects.filter(sair=BulunanSair).order_by('-olusturma_tarihi')
    sayfa_adi = f"Tüm {BulunanSair.title} Eserleri"
    paginator = Paginator(siir, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)
    siirRandom = Siirler.objects.order_by('?')[:8]
    sairRandomsag = Sairler.objects.order_by('?')[:8]
    title = "En Güzel Sözler"
    description = "Aradığınız en anlamlı tüm sözler yok yok hemen takip edip paylaşabilirsiniz."
    keywords = "anlamlı sözler, ilginç sözler, özlü sözler, güzel sözler, en güzel sözler"




    context = {
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'siirRandom': siirRandom,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/sozler/soz_coklu_sayfa.html', context)




def alt_kategori_detail(request,  alt_kategori_slug):
    alt_kategori = get_object_or_404(SiirAltKategori, sozler_slug=alt_kategori_slug)
    siir = Sozler.objects.filter(alt_kategorisi=alt_kategori).order_by('-olusturma_tarihi')
    sayfa_adi = alt_kategori.sozler_title

    paginator = Paginator(siir, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?')[:8]
    CokOkunanSiirler = Siirler.objects.order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, soz=True)
    siirRandom = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    context = {
        'icerik': icerik,
        'title': alt_kategori.sozler_title,
        'description': alt_kategori.meta_description_soz,
        'keywords': alt_kategori.keywords_soz,
        'sayfa_adi': f"En Güzel {sayfa_adi}",
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandom': siirRandom,
        'sairRandomsag': sairRandomsag,

    }
    return render(request, 'system/sozler/soz_coklu_sayfa.html', context)




def bunlarLazim(Sairmi):
    siirRandomsag = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sozRandom = Sozler.objects.filter(aktif=True,status="Yayinda").order_by('?').first()
    siirRandom = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?').first()
    yazarRandom = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?').first()
    hikayeRandom = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?').first()
    return siirRandomsag,sairRandomsag,sozRandom,siirRandom, yazarRandom, hikayeRandom



def soz_detail(request,  soz_slug):
    siir = get_object_or_404(Sozler, slug=soz_slug)
    siir.okundu()
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,soz=True)
    siirRandomsag, sairRandomsag, sozRandom, siirRandom, yazarRandom, hikayeRandom=bunlarLazim(siir)

    if not isinstance(request.user, AnonymousUser):
        favoride = FavoriSozler.objects.filter(soz=siir, kullanici=request.user).exists()
        begenildi = BegeniSozler.objects.filter(soz=siir, kullanici=request.user).exists()
    else:
        favoride = False
        begenildi = False

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
        'sozRandom': sozRandom,
        'favoride': favoride,
        'begenildi': begenildi,
        'siirRandom': siirRandom,
        'yazarRandom': yazarRandom,
        'hikayeRandom': hikayeRandom,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,  # popülerKategoriler
    }
    return render(request, 'system/sozler/soz_detail.html', context)




@login_required
def favori(request, soz_id):
    siir = get_object_or_404(Sozler, id=soz_id)
    FavoriSozler.objects.get_or_create(soz=siir, kullanici=request.user)
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)
@login_required
def favori_kaldir(request, soz_id):
    siir = get_object_or_404(Sozler, id=soz_id)
    FavoriSozler.objects.filter(soz=siir, kullanici=request.user).delete()
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)



@login_required
def begen(request, soz_id):
    siir = get_object_or_404(Sozler, id=soz_id)
    BegeniSozler.objects.get_or_create(soz=siir, kullanici=request.user)
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)
@login_required
def begen_kaldir(request, soz_id):
    siir = get_object_or_404(Sozler, id=soz_id)
    BegeniSozler.objects.filter(soz=siir, kullanici=request.user).delete()
    return redirect('sozler:soz_slug',  soz_slug=siir.slug)


