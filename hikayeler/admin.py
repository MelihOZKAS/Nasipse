from django.contrib import admin
from .models import Hikayeler,HikayeAltKategori
# Register your models here.
class HikayeAltKategoriAdmin(admin.ModelAdmin):
    list_display = ("alt_kategori_adi","aktif","banner",)
    prepopulated_fields = {'slug': ('alt_kategori_adi',)}
    search_fields = ("alt_kategori_adi",)
    list_filter = ("alt_kategori_adi","aktif","banner",)
    list_editable = ("aktif","banner",)



admin.site.register(HikayeAltKategori, HikayeAltKategoriAdmin)




class HikayeAdmin(admin.ModelAdmin):
    list_display = ("title","yazar","Model","okunma_sayisi","status","banner","small_banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("yazar","status","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)


admin.site.register(Hikayeler, HikayeAdmin)