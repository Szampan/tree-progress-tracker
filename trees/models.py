# from tokenize import blank_re
from email.policy import default
import uuid
import pathlib

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from tools import *

def user_directory_path(instance, filename):                  # do usunięcia albo przerobienia
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'images/user_{instance.entry.tree.owner.id}/{filename}'

def tree_images_upload_handler(instance, filename):             # later: make it better
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())   # uuid1 -> uuid + timestamp
    return f'images/user_{instance.owner.id}/{new_fname}{fpath.suffix}'

def album_path_handler(instance, filename):
    return f'images/album_{instance.album.id}/{filename}'


class Tree(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    specie = models.CharField(max_length=50, blank=True)
    specie_latin = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # date_planted = models.DateField(blank=True)                   #?
    image = models.ImageField(upload_to=tree_images_upload_handler, blank=True)    # later: upload photo or choose among images assigned do entries
    is_bonsai = models.BooleanField(default=False)

    # tags: bonsai, decidous, conifer, indoor, outdoor
    # location = models.CharField(max_length=200)
    # height = models.IntegerField()
    # diameter = models.IntegerField()

    def __str__(self):
        return self.name
    
class ImageAlbum(models.Model):     #ImageAlbom powinien być przypięty do Entry a nie odwrotnie?
    def default(self):
        return self.images.filter(default=True).first()

    def show_images(self):
        return self.images.all()
    
    # def thumbnails(self):
    #     return self.images.filter(width__lt=100, length_lt=100)

class Image(models.Model):
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=album_path_handler, blank=True)
    default = models.BooleanField(default=False)    


class Entry(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    album = models.OneToOneField(ImageAlbum, on_delete=models.CASCADE, related_name='entry', blank=True, null=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)   # settings.AUTH_USER_MODEL instead of User?
    date_added = models.DateTimeField(auto_now_add=True)
    date_photos_taken = models.DateField()
    comment = models.TextField(max_length=1000, blank=True, null=True)
    # image = models.ImageField(upload_to=tree_images_upload_handler, blank=True)
    

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        date = str(self.date_photos_taken.strftime('%Y-%m-%d')) if self.date_photos_taken else ''
        return f'{self.tree.name}: ' + date

    # def save(self, *args, **kwargs):
    #     if not self.album:
    #         self.album = ImageAlbum.objects.create()

    #         lol('◘◘◘ Entry album:')
    #         lol(self.album)
    #     super().save(*args, **kwargs)



# def get_image_filename(filename):   
#     # slug = slugify()
#     return f"post_images/{filename}"

class Images(models.Model):     # later: delete. Image is new model instead of Images.    
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name='Image test')  #null=True ?
    default = models.BooleanField(default=False)    
    # default_for_tree = models.BooleanField(default=False)  # Later ?

    class Meta:
        verbose_name_plural = 'imagessss_old'



