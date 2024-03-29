from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import AnasayfaKeyler,Siirler,SiirAltKategori,Begeni,Favori,WhatsappReklam
import random
from sairler.models import Sairler
from sozler.models import Sozler
from sozler.views import bunlarLazim
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
def siir_home_detail(request):
   # tum_alt_kategoriler = SiirAltKategori.objects.all()
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,aktif=True,siir=True)
    populersiir = Siirler.objects.filter(aktif=True,status="Yayinda", small_banner=True)[:15]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-okunma_sayisi')[:15]
    son_eklenen_siirler = Siirler.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:6]
    siirRandom = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]


    title = "En Güzel Şiirler"
    description = "En Güzel Şiirler’ deki şiir koleksiyonumuzda, farklı şairlerin şiir ve sözlerini keşfedin. Her bir şiir, duyguları ve düşünceleri benzersiz bir şekilde ifade eder."
    keywords = "şiir, aşk şiirleri, atatürk şiirleri, 10 kasım şiirleri, sevgiliye şiirler, anne şiirleri, baba şiirleri, kısa şiirler, kısa aşk şiirleri"


    context = {
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,#popülerKategoriler
        'CokOkunanSiirler': CokOkunanSiirler,
        'son_eklenen_siirler': son_eklenen_siirler,
        'siirRandomsag': siirRandom,
        'sairRandomsag': sairRandomsag,
        'populersiir': populersiir,
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/siir/siir_home.html', context)

def all_Kategori(request):
    tum_alt_kategoriler = SiirAltKategori.objects.filter(aktif=True,siir=True)
    random_populer = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, aktif=True, siir=True)
    siirRandom = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]

    context = {
        'tum_alt_kategoriler': tum_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,  # popülerKategoriler
        'siirRandomsag': siirRandom,
        'sairRandomsag': sairRandomsag,

    }
    return render(request, 'system/siir/tum_siir_kategori.html', context)




@login_required
def favori(request, siir_id):
    siir = get_object_or_404(Siirler, id=siir_id)
    Favori.objects.get_or_create(siir=siir, kullanici=request.user)
    return redirect('siir:siir_detail', siir_slug=siir.slug)
@login_required
def favori_kaldir(request, siir_id):
    siir = get_object_or_404(Siirler, id=siir_id)
    Favori.objects.filter(siir=siir, kullanici=request.user).delete()
    return redirect('siir:siir_detail', siir_slug=siir.slug)



@login_required
def begen(request, siir_id):
    siir = get_object_or_404(Siirler, id=siir_id)
    Begeni.objects.get_or_create(siir=siir, kullanici=request.user)
    return redirect('siir:siir_detail', siir_slug=siir.slug)
@login_required
def begen_kaldir(request, siir_id):
    siir = get_object_or_404(Siirler, id=siir_id)
    Begeni.objects.filter(siir=siir, kullanici=request.user).delete()
    return redirect('siir:siir_detail', siir_slug=siir.slug)



def coklu_sayfa(request):
    url_name = request.resolver_match.url_name

    if url_name == 'populer-siirler':
        siir = Siirler.objects.filter(small_banner=True).order_by('?')
        sayfa_adi = "Popüler Şiirler - enguzelsiirler.com"
        title = "En Popüler Şiirler - enguzelsiirler.com"
        description = "Değerli şairlerimizin popüler şiirleri dev şiir arşivi"
        keywords = "şiir, meşhur şiirler, pöpüler şiirler, aşk şiirleri, atatürk şiirleri"
    elif url_name == 'cok-okunan-siirler':
        siir = Siirler.objects.filter(small_banner=True).order_by('-okunma_sayisi')
        sayfa_adi = "En Çok Okunan Şiirler - enguzelsiirler.com"
        title = "En Çok Okunan Şiirler"
        description = "Değerli şairlerimizin en çok okunan şiirlerinin listesi"
        keywords = "şiir, kısa aşk şiirleri, az bilinen aşk şiirleri, romantik şiirler, sevgiliye şiir"
    elif url_name == 'en-son-eklenen-siirler':
        siir = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-olusturma_tarihi')
        sayfa_adi = "En Son Eklenen Şiirler - enguzelsiirler.com"
        title = "En Son Eklenen Şiirler"
        description = "Sitemize en son eklenen şiirlerin sıralaması aradığınız tüm şiirler burada"
        keywords = "şiir, meşhur şiirler, pöpüler şiirler, aşk şiirleri, atatürk şiirleri"





    paginator = Paginator(siir, 10) # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(aktif=True,status="Yayinda",small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,siir=True)
    siirRandomsag = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]

    if page_number is None:
        page_number = ""

    title = f"{title} - {page_number}"
    description = f"{description} - Sayfa {page_number}"

    context = {
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/siir/coklu_sayfa.html', context)



def alt_kategori_detail(request,  alt_kategori_slug):
    alt_kategori = get_object_or_404(SiirAltKategori, slug=alt_kategori_slug)
    siir = Siirler.objects.filter(alt_kategorisi=alt_kategori).order_by('?')
    sayfa_adi = f"En Güzel {alt_kategori.alt_kategori_adi}"

    paginator = Paginator(siir, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,siir=True)
    siirRandomsag = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]

    if page_number is None:
        page_number = ""

    context = {
        'icerik': icerik,
        'alt_kategori': alt_kategori,
        'sayfa_adi': sayfa_adi,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'page_number': page_number,
    }
    return render(request, 'system/siir/altkategoridetay.html', context)



def sairTumeserleri(request,  sair_slug):
    BulunanSair = get_object_or_404(Sairler, slug=sair_slug)
    siir = Siirler.objects.filter(sair=BulunanSair,status="Yayinda",aktif=True).order_by('?')
    soz = Sozler.objects.filter(sair=BulunanSair,status="Yayinda",aktif=True).order_by('?')
    sayfa_adi = f"Tüm {BulunanSair.title} Eserleri"

    Karma_yapilmis_hali = list(chain(siir, soz))

    paginator = Paginator(Karma_yapilmis_hali, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,siir=True)
    siirRandomsag = Siirler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]
    sairRandomsag = Sairler.objects.filter(aktif=True,status="Yayinda").order_by('?')[:8]


    if page_number is None:
        page_number = ""

    title = f"{BulunanSair.title} Tüm Şiir ve Sözleri - {page_number}"
    description = f"{BulunanSair.meta_description} - Sayfa {page_number}"
    keywords = f"{BulunanSair.keywords}"

    context = {
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'system/siir/sair-tum-eserleri.html', context)


def siir_detail(request,  siir_slug):
    siir = get_object_or_404(Siirler,  slug=siir_slug)
    siir.okundu()
    if not isinstance(request.user, AnonymousUser):
        favoride = Favori.objects.filter(siir=siir, kullanici=request.user).exists()
        begenildi = Begeni.objects.filter(siir=siir, kullanici=request.user).exists()
    else:
        favoride = False
        begenildi = False
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True,siir=True)
    random_Soz = Sozler.objects.filter(small_banner=True).order_by('?').first()
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
        'favoride': favoride,
        'begenildi': begenildi,
        'sozRandom': sozRandom,
        'siirRandom': siirRandom,
        'yazarRandom': yazarRandom,
        'hikayeRandom': hikayeRandom,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
    }
    return render(request, 'system/siir/siir_detail.html', context)
@csrf_exempt
def toplu_ekleme_wp(request):
    TelefonNoList = []
    #MesajListesi = ["Dünyada en çok okunan Türk şiiri olan Orhan Veli Kanık'ın 'Anlatamıyorum' şiirini mutlaka okumalısın. Şiir, insanın duygularını ve düşüncelerini kelimelere dökmekte zorlandığını anlatıyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Orhan Veli Kanık'ın 'Anlatamıyorum' şiiri, Türkçe şiirin en güzel örneklerinden biri. Şiir, kelimelerle ifade edilemeyen duyguları ve düşünceleri anlatıyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Orhan Veli Kanık'ın büyülü dizesiyle tanışın: 'Anlatamıyorum.' Bu şiir sadece birkaç kelimeyle ifade edebileceğiniz derin duyguların ifadesidir. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Orhan Veli Kanık'ın unutulmaz şiiri 'Anlatamıyorum' ile hislerinize tercüman olun. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Dilimizden düşmeyen, gönlümüzden silinmeyen bir şiir: Orhan Veli Kanık'ın 'Anlatamıyorum' şiirine göz atın! https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Orhan Veli Kanık'ın ölümsüz şiiri 'Anlatamıyorum' ile iç dünyanıza yolculuk yapın. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Türk edebiyatının en etkileyici şiirlerinden biri: Orhan Veli Kanık'ın 'Anlatamıyorum.' Siz de bu şiiri okumalısınız! https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiiri okudun mu? Dünyanın en güzel aşk şiiri olduğunu söylüyorlar. Bakalım sen de katılıyor musun? https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Senin için bir şiir buldum. Bu şiir, dünyada en çok okunan Türk şiiriymiş. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk şiirinin en büyük ustalarından biri olan Orhan Veli Kanık’ın eseri. Dünyada en çok okunan Türk şiiri olma unvanını taşıyor. Bu şiiri okumak istersen. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk edebiyatının en önemli isimlerinden biri olan Orhan Veli Kanık’ın kaleme aldığı bir başyapıt. Dünyada en çok okunan Türk şiiri olarak biliniyor. Bu şiiri merak ediyorsan. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk kültürünün en değerli miraslarından biri olan Orhan Veli Kanık’ın yazdığı bir şaheser. Dünyada en çok okunan Türk şiiri olarak tanınıyor. Bu şiiri görmek istersen. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk sanatının en güzel örneklerinden biri olan Orhan Veli Kanık’ın ortaya çıkardığı bir harika. Dünyada en çok okunan Türk şiiri olarak anılıyor. Bu şiiri incelemek istersen. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk dilinin en yetkin kullanıcılarından biri olan Orhan Veli Kanık’ın oluşturduğu bir mucize. Dünyada en çok okunan Türk şiiri olarak övülüyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk tarihinin en etkili şairlerinden biri olan Orhan Veli Kanık’ın yarattığı bir efsane. Dünyada en çok okunan Türk şiiri olarak saygı görüyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk düşüncesinin en özgün temsilcilerinden biri olan Orhan Veli Kanık’ın aktardığı bir mesaj. Dünyada en çok okunan Türk şiiri olarak ilgi çekiyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk duyarlılığının en samimi yansıtıcılarından biri olan Orhan Veli Kanık’ın paylaştığı bir duygu. Dünyada en çok okunan Türk şiiri olarak beğeni topluyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","Bu şiir, Türk estetiğinin en zarif yaratıcılarından biri olan Orhan Veli Kanık’ın sunduğu bir güzellik. Dünyada en çok okunan Türk şiiri olarak hayran bırakıyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/","u şiir, Türk sanatının en büyük katkılarından biri olan Orhan Veli Kanık’ın yaptığı bir yenilik. Dünyada en çok okunan Türk şiiri olarak etkiliyor. https://www.enguzelsiirler.com/siir/orhan-veli-kanik-anlatamyorum-siiri/"]
    MesajListesi = ["Şiirlerle dolu bir dünyaya adım atın! https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Şiir severler için özel bir yer, https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Siz de şiirlerin büyülü dünyasına katılmak ister misiniz?  https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Şairlerin en özel eserleri sadece bir tıklama uzaklıkta! https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Şairlerin en özel eserleri sadece bir tıklama uzaklıkta! https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Edebiyatın en güzel yanlarını keşfetmek için buradayız. https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","En güzel şiirleri keşfetmeye hazır mısın? https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Türk edebiyatından en seçkin şiirler, tek bir adreste https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Şairlerin dünyasına adım atmak için https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","Şiirle sevdiklerini mutlu etmek için https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*","En güzel şiirlere göz atın https://www.enguzelsiirler.com _Sitemiz Yeni Açılmıştır_ bizi takip edip bize destek olursanız çok seviniriz. Bu mesaj sadece 1 kereliktir *rahatsızlık verdiysek çok özür dileriz.*"]
    TelefonNoList = list(set(TelefonNoList))

    reklamlar = []
    for telefon_no in TelefonNoList:
        if not WhatsappReklam.objects.filter(TelefonNo=telefon_no).exists():
            mesaj = random.choice(MesajListesi)
            reklam = WhatsappReklam(TelefonNo=telefon_no, Mesaj=mesaj)
            reklamlar.append(reklam)

    WhatsappReklam.objects.bulk_create(reklamlar)
    return HttpResponse("ŞükürlerOlsun bitti")

@csrf_exempt
def wp_cek(request):
    reklam = WhatsappReklam.objects.filter(atildi=False).first()
    if reklam is not None:
        reklam.atildi = True
        reklam.save()
        return HttpResponse(f"{reklam.TelefonNo}|{reklam.Mesaj}")
    else:
        return HttpResponse("Tüm reklamlar gönderildi.")



@csrf_exempt
def indexing_var_mi(request):
    post = Siirler.objects.filter(indexing=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.indexing = False
        post.save()
        return HttpResponse(f"https://www.enguzelsiirler.com/siir/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")