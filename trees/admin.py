from django.contrib import admin
from .models import Tree, Entry, Image, ImageAlbum 

class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1 

class TreeAdmin(admin.ModelAdmin):
    inlines = [EntryInline]

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ImageAlbumAdmin(admin.ModelAdmin):
    inlines = [EntryInline, ImageInline]

admin.site.register(Tree, TreeAdmin)
admin.site.register(Entry)
admin.site.register(ImageAlbum, ImageAlbumAdmin)
admin.site.register(Image)
