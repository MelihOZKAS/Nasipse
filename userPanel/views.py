from django.shortcuts import render,redirect,get_object_or_404
from sairler.models import Sairler
from siirler.models import Siirler,SiirAltKategori,Begeni,Favori
from sozler.models import Sozler,FavoriSozler,BegeniSozler
from hikayeler.models import Hikayeler,FavoriHikayeler,BegeniHikayeler
from sozler.views import bunlarLazim
from .models import CustomUser,FavoriSairUser,BegeniSairUser
import random
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.contrib.auth.models import AnonymousUser



@login_required(login_url = 'giris-yap')
def konsol_home_detail(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    SiirToplami = Siirler.objects.filter(yazar=request.user).count()
    HikayeToplami = Hikayeler.objects.filter(yazar=request.user).count()
    SozToplami = Sozler.objects.filter(yazar=request.user).count()

    context = {'name': f"{first_name} {last_name}",
               'email':email,
               'SiirToplami':SiirToplami,
               'HikayeToplami':HikayeToplami,
               'SozToplami':SozToplami,
               }
    return render(request, 'system/user/panel.html',context)


@login_required(login_url = 'giris-yap')
def SiirDetayListesi(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    siirler = Siirler.objects.filter(yazar=request.user)
    siirler_listesi = []
    for siir in siirler:
        favori_sayisi = Favori.objects.filter(siir=siir).count()
        begeni_sayisi = Begeni.objects.filter(siir=siir).count()
        siirler_listesi.append({
            'siir': siir,
            'favori_sayisi': favori_sayisi,
            'begeni_sayisi': begeni_sayisi,
        })

    context = {
        'siirler_listesi': siirler_listesi,
        'name': f"{first_name} {last_name}",
        'email': email,
    }
    return render(request, 'system/user/siirdetaylistesi.html', context)




@login_required(login_url = 'giris-yap')
def SozDetayListesi(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    sozler = Sozler.objects.filter(yazar=request.user)
    siirler_listesi = []
    for soz in sozler:
        favori_sayisi = FavoriSozler.objects.filter(soz=soz).count()
        begeni_sayisi = BegeniSozler.objects.filter(soz=soz).count()
        siirler_listesi.append({
            'siir': soz,
            'favori_sayisi': favori_sayisi,
            'begeni_sayisi': begeni_sayisi,
        })

    context = {
        'siirler_listesi': siirler_listesi,
        'name': f"{first_name} {last_name}",
        'email': email,
    }
    return render(request, 'system/user/sozdetaylistesi.html', context)


@login_required(login_url = 'giris-yap')
def HikayeDetayListesi(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    hikayeler = Hikayeler.objects.filter(yazar=request.user)
    siirler_listesi = []
    for hikaye in hikayeler:
        favori_sayisi = FavoriHikayeler.objects.filter(hikayeler=hikaye).count()
        begeni_sayisi = BegeniHikayeler.objects.filter(hikayeler=hikaye).count()
        siirler_listesi.append({
            'siir': hikaye,
            'favori_sayisi': favori_sayisi,
            'begeni_sayisi': begeni_sayisi,
        })

    context = {
        'siirler_listesi': siirler_listesi,
        'name': f"{first_name} {last_name}",
        'email': email,
    }
    return render(request, 'system/user/hikayedetaylistesi.html', context)







@login_required(login_url='giris-yap')
def TumFavoriler(request):
    url_name = request.resolver_match.url_name

    if url_name == 'favori-siirler':
        favorilerim = Siirler.objects.filter(favori__kullanici=request.user)
        Favori_Name = "Favoriye Aldığınız Şiirler"
    elif url_name == 'favori-sozler':
        favorilerim = Sozler.objects.filter(favorisozler__kullanici=request.user)
        Favori_Name = "Favoriye Aldığınız Sözler"
    elif url_name == 'favori-hikayeler':
        favorilerim = Hikayeler.objects.filter(favorihikayeler__kullanici=request.user)
        Favori_Name = "Favoriye Aldığınız Hikayeler"
    elif url_name == 'favori-sair':
        favorilerim = Sairler.objects.filter(favorisair__kullanici=request.user)
        Favori_Name = "Favoriye Aldığınız Şairler"
    elif url_name == 'favori-kullanici':
        favorilerim = CustomUser.objects.filter(favorisairuser_sairuser__kullanici=request.user)
        #favoriUser = CustomUser.objects.filter(favorisairuser__favorisairuser_kullanici=request.user)
        print(favorilerim)

        Favori_Name = "Favoriye Aldığınız Üye Yazarlar"



    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    context = {'favorilerim': favorilerim,
               'name': f"{first_name} {last_name}",
               'email': email,
               'Favori_Name': Favori_Name,
               }
    return render(request, 'system/user/favori-siirler.html', context)




@login_required(login_url='giris-yap')
def TumBegeni(request):
    url_name = request.resolver_match.url_name

    if url_name == 'begeni-siirler':
        Begenilerim = Siirler.objects.filter(begeni__kullanici=request.user)
        Begeni_Name = "Beğeniye Aldığınız Şiirler"
    elif url_name == 'begeni-sozler':
        Begenilerim = Sozler.objects.filter(begenisozler__kullanici=request.user)
        Begeni_Name = "Beğeniye Aldığınız Sözler"
    elif url_name == 'begeni-hikayeler':
        Begenilerim = Hikayeler.objects.filter(begenihikayeler__kullanici=request.user)
        Begeni_Name = "Beğeniye Aldığınız Hikayeler"
    elif url_name == 'begeni-sairler':
        Begenilerim = Sairler.objects.filter(begenisair__kullanici=request.user)
        Begeni_Name = "Beğeniye Aldığınız Şairler"
    elif url_name == 'begeni-kullanici':
        Begenilerim = CustomUser.objects.filter(begenisairuser_sairuser__kullanici=request.user)
        #favoriUser = CustomUser.objects.filter(favorisairuser__favorisairuser_kullanici=request.user)
        print(Begenilerim)
        Begeni_Name = "Beğeniye Aldığınız Üye Yazarlar"



    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    context = {'Begenilerim': Begenilerim,
               'name': f"{first_name} {last_name}",
               'email': email,
               'Begeni_Name': Begeni_Name,
               }
    return render(request, 'system/user/begeni-user.html', context)






def yazar_detail(request,  yazar):
    sair = get_object_or_404(CustomUser, slug=yazar)
    siir = Siirler.objects.filter(status="Yayinda", aktif=True).order_by('?').first()
    random_Soz = Sozler.objects.filter(small_banner=True).order_by('?').first()
    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True, aktif=True, siir=True)
    title = "En Güzel Şiirler Üye Detay"
    description = "Üyelerimizin eserleri ve biyografilerine ulaşabilirsiniz. Üyelerimizin şiirlerini ve hayat hikayelerini keşfedebilir, üyelerimizin eserlerine buradan ulaşabilirsiniz."
    keywords = "şiir, aşk şiirleri, atatürk şiirleri, öğretmenler günü şiirleri, sevgiliye şiirler, anne şiirleri, baba şiirleri, kısa şiirler, kısa aşk şiirleri"

    if not isinstance(request.user, AnonymousUser):
        favoride = FavoriSairUser.objects.filter(sairUser=sair, kullanici=request.user).exists()
        begenildi = BegeniSairUser.objects.filter(sairUser=sair, kullanici=request.user).exists()
    else:
        favoride = False
        begenildi = False
    siirRandomsag, sairRandomsag, sozRandom, siirRandom, yazarRandom, hikayeRandom= bunlarLazim(siir)

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
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,  # popülerKategoriler
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'system/user/yazar_detail.html', context)



def yazar_tum_eserleri(request,  yazar):
    BulunanSair = get_object_or_404(CustomUser, slug=yazar)
    siir = Siirler.objects.filter(yazar=BulunanSair,status="Yayinda",aktif=True).order_by('?')
    soz = Sozler.objects.filter(yazar=BulunanSair,status="Yayinda",aktif=True).order_by('?')
    hikaye = Hikayeler.objects.filter(yazar=BulunanSair,status="Yayinda",aktif=True).order_by('?')
    sayfa_adi = f"Tüm {BulunanSair.first_name} {BulunanSair.last_name} Eserleri"

    Karma_yapilmis_hali = list(chain(siir, soz, hikaye))
    paginator = Paginator(Karma_yapilmis_hali, 10)  # 10 kayıtlık sayfalar oluştur
    page_number = request.GET.get('sayfa')
    icerik = paginator.get_page(page_number)

    random_populer = Siirler.objects.filter(small_banner=True).order_by('?')[:6]
    CokOkunanSiirler = Siirler.objects.order_by('-okunma_sayisi')[:15]

    tum_banner_alt_kategoriler = SiirAltKategori.objects.filter(banner=True)
    siirRandomsag = Siirler.objects.order_by('?')[:8]
    sairRandomsag = Sairler.objects.order_by('?')[:8]


    if page_number is None:
        page_number = ""


    context = {
        'icerik': icerik,
        'sayfa_adi': sayfa_adi,
        'TumSiirBannerKategorileri': tum_banner_alt_kategoriler,
        'CokOkunanSiirler': CokOkunanSiirler,
        'random_populer': random_populer,
        'siirRandomsag': siirRandomsag,
        'sairRandomsag': sairRandomsag,
        'page_number': page_number,

    }
    return render(request, 'system/user/yazar-tum-eserleri.html', context)



@login_required(login_url='giris-yap')
def SiirEkle(request):
    if request.method == 'POST':
        title = request.POST['title']
        alt_kategorisi = request.POST.getlist('alt_kategorisi')
        icerik = request.POST['icerik']
        hakkinda = request.POST['hakkinda']
        print("Nasip1")

        icerik = icerik.replace('\n', '<br>')

        # form verilerini kullanarak bir Siirler örneği oluşturun
        siir = Siirler.objects.create(
            title=title,
            yazar=request.user,
            icerik=icerik,
            hakkinda=hakkinda,
            Model='Şiirler',
            status='Kontrol',
            usermi=True,
            aciklama="Kontrol Bekleniyor."
        )

        # alt kategorileri ayarlayın
        for alt_kategori_id in alt_kategorisi:
            siir.alt_kategorisi.add(alt_kategori_id)

        # kaydedin
        siir.save()
        print("Nasip2")



    TumAltKategori = SiirAltKategori.objects.all()
    Turu = "Değerli Şiirlerinizi Bizlerle Paylaşın!"
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    context = {
               'name': f"{first_name} {last_name}",
               'email': email,
               'TumAltKategori': TumAltKategori,
               'Turu': Turu,
               }
    return render(request, 'system/user/Nasipse-siir-ekle.html', context)


@login_required(login_url='giris-yap')
def SozEkle(request):
    if request.method == 'POST':
        title = request.POST['title']
        alt_kategorisi = request.POST.getlist('alt_kategorisi')
        icerik = request.POST['icerik']

        print("Nasip1")

        # form verilerini kullanarak bir Siirler örneği oluşturun
        soz = Sozler.objects.create(
            title=title,
            yazar=request.user,
            icerik=icerik,
            Model='Sözler',
            status='Kontrol',
            usermi=True,
            aciklama="Kontrol Bekleniyor."
        )

        # alt kategorileri ayarlayın
        for alt_kategori_id in alt_kategorisi:
            soz.alt_kategorisi.add(alt_kategori_id)

        # kaydedin
        soz.save()



    TumAltKategori = SiirAltKategori.objects.all()
    Turu = "Değerli Sözlerinizi Bizlerle Paylaşın!"
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    context = {
               'name': f"{first_name} {last_name}",
               'email': email,
               'TumAltKategori': TumAltKategori,
               'Turu': Turu,
               }
    return render(request, 'system/user/Nasipse-soz-ekle.html', context)





@login_required
def favori(request, yazar_id):
    siir = get_object_or_404(CustomUser, id=yazar_id)
    FavoriSairUser.objects.get_or_create(sairUser=siir, kullanici=request.user)
    return redirect('konsol:blog-yazar-detay', yazar=siir.slug)
@login_required
def favori_kaldir(request, yazar_id):
    siir = get_object_or_404(CustomUser, id=yazar_id)
    FavoriSairUser.objects.filter(sairUser=siir, kullanici=request.user).delete()
    return redirect('konsol:blog-yazar-detay', yazar=siir.slug)



@login_required
def begen(request, yazar_id):
    siir = get_object_or_404(CustomUser, id=yazar_id)
    BegeniSairUser.objects.get_or_create(sairUser=siir, kullanici=request.user)
    return redirect('konsol:blog-yazar-detay', yazar=siir.slug)
@login_required
def begen_kaldir(request, yazar_id):
    siir = get_object_or_404(CustomUser, id=yazar_id)
    BegeniSairUser.objects.filter(sairUser=siir, kullanici=request.user).delete()
    return redirect('konsol:blog-yazar-detay', yazar=siir.slug)


