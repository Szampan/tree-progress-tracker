from django.contrib import admin

from .models import Tree, Entry, Image, ImageAlbum, Images
admin.site.register(Tree)
admin.site.register(Entry)
admin.site.register(ImageAlbum)
admin.site.register(Image)

admin.site.register(Images)     # Old. Delete.


# class EntriesInline(admin.TabularInline):
#     model = Entry
#     extra = 1

# class TreeAdmin(admin.ModelAdmin):
#     inlines = [EntriesInline]