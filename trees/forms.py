from django import forms
from .models import Tree, Entry, ImageAlbum, Image, Images

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'specie', 'specie_latin', 'description', 'is_bonsai']


class EntryForm(forms.ModelForm):
    """ Comment and date_photos_taken defined here, because of FullEntryForm """
    comment = forms.CharField(label="Comment", required=False)
    date_photos_taken = forms.DateField(label="Date photos taken", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Entry
        fields = ['comment', 'date_photos_taken']

    def __init__(self, *args, **kwargs):
        """ Save the request with the form so it can be accessed in clean_*() """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class FullEntryForm(EntryForm):
    # Jeśli wyskakuje błąd, to może być kwestia braku zdefiniowania odpowiedniego albumu
    # ImageForm zamiast fileField?
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        # model = ImageAlbum   # tego nie było / old
        model = Image   # new
        fields = EntryForm.Meta.fields + ['images',]
    #     # fields = ['images']

    # Save all images to the album
    def save(self, commit=True, *args, **kwargs):
        album = super().save(commit=False)
        album.user = self.request.user
        album.save()
        for image in self.cleaned_data['images']:
            album.images.create(image=image)
        return album


    




# from django import forms
# from .models import Tree, Entry, Images


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label="Image")
#     class Meta:
#         model = Images
#         fields = ('image', )