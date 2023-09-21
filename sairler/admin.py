from django.contrib import admin
from .models import Sairler
# Register your models here.


class SairlerAdmin(admin.ModelAdmin):
    list_display = ("title","yazar","Model","okunma_sayisi","status","banner","small_banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("yazar","status","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)


admin.site.register(Sairler, SairlerAdmin)