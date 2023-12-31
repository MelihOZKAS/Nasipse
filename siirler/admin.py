from django.contrib import admin
from .models import Siirler,AnasayfaKeyler,SiirAltKategori,WhatsappReklam

# Register your models here.





class SiirAltKategoriAdmin(admin.ModelAdmin):
    list_display = ("alt_kategori_adi","keywords","keywords_soz","siir","soz","aktif","banner",)
    prepopulated_fields = {'slug': ('alt_kategori_adi',), 'sozler_slug': ('sozler_title',)}
    search_fields = ("alt_kategori_adi",)
    list_filter = ("alt_kategori_adi","aktif","banner",)
    list_editable = ("aktif","banner","siir","soz",)



admin.site.register(SiirAltKategori, SiirAltKategoriAdmin)




class SiirlerAdmin(admin.ModelAdmin):
    list_display = ("title","yazar","Model","okunma_sayisi","sair","status","banner","small_banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("yazar","sair","status","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)


admin.site.register(Siirler, SiirlerAdmin)



class KeyAdmin(admin.ModelAdmin):
    list_display = ("title","meta_title",)


admin.site.register(AnasayfaKeyler, KeyAdmin)



class WhatsappReklamAdmin(admin.ModelAdmin):
    list_display = ("TelefonNo","Mesaj","atildi",)
    search_fields = ("TelefonNo","Mesaj",)
    list_filter = ("atildi",)
    list_editable = ("atildi",)

admin.site.register(WhatsappReklam, WhatsappReklamAdmin)