from django.contrib import admin

# Register your models here.

from .models import Sozler

class SozlerAdmin(admin.ModelAdmin):
    list_display = ("title","yazar","sair","status","banner","small_banner","aktif",)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ("title",)
    list_filter = ("yazar","sair","status","aktif","banner","small_banner",)
    list_editable = ("status","aktif","banner","small_banner",)


admin.site.register(Sozler, SozlerAdmin)