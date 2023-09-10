from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,AbstractUser
from django.db import models
from django.utils.text import slugify
from django.conf import settings

from Nasipsiir.custom_storages import ImageSettingStorage


def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"
class CustomUserManager(BaseUserManager):
    def create_user(self, first_name,last_name,username,email,phone_number,hakkinda_ozet,hakkinda_detay, password=None):
        if not phone_number:
            raise ValueError('Kullanıcılar için telefon numarası gerekli')
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            hakkinda_ozet=hakkinda_ozet,
            hakkinda_detay=hakkinda_detay,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name,username,email,phone_number, hakkinda_ozet,hakkinda_detay,password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            hakkinda_ozet=hakkinda_ozet,
            hakkinda_detay=hakkinda_detay,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    hakkinda_ozet = models.TextField(null=True,blank=True)
    hakkinda_detay = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    Kayit_Tarihi =models.DateTimeField(auto_now_add=True)
    Son_Giris_Tarihi =models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    # kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,help_text=HELP_TEXTS["kapak_resmi"])
    kapak_resmi = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(), null=True, blank=True)
    okunma_sayisi = models.PositiveBigIntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['hakkinda_ozet', 'hakkinda_detay','first_name','last_name','phone_number','email']


    def okundu(self):
        self.okunma_sayisi += 1
        self.save()
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.id}")
            super().save(*args, **kwargs)


class FavoriSairUser(models.Model):
    sairUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorisairuser_sairuser')
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorisairuser_kullanici')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

class BegeniSairUser(models.Model):
    sairUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='begenisairuser_sairuser')
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='begenisairuser_kullanici')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)



class YorumSairUser(models.Model):
    sairUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='yorumlarSairUser')
    yazar = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,related_name='yorumlarSairYazar')
    icerik = models.TextField()
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
