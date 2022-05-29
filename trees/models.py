# from tokenize import blank_re
import uuid
import pathlib

from django.db import models
from django.contrib.auth.models import User
# from django.template.defaultfilters import slugify

def user_directory_path(instance, filename):                  # do usunięcia
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'static/images/user_{instance.owner.id}/{filename}'

def tree_images_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1())   # uuid1 -> uuid + timestamp
    return f'static/images/user_{instance.owner.id}/{new_fname}{fpath.suffix}'


class Tree(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    specie = models.CharField(max_length=50, blank=True)
    specie_latin = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # date_planted = models.DateField(blank=True)                   #?
    image = models.ImageField(upload_to=tree_images_upload_handler, blank=True)    # later
    is_bonsai = models.BooleanField(default=False)

    # tags: bonsai, decidous, conifer, indoor, outdoor
    # location = models.CharField(max_length=200)
    # height = models.IntegerField()
    # diameter = models.IntegerField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_photos_taken = models.DateTimeField(blank=True)
    comment = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to=tree_images_upload_handler, blank=True)
    
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.comment
