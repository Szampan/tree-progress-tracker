from django import forms
from .models import Tree, Entry, ImageAlbum, Image 

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
    pass
    # Jeśli wyskakuje błąd, to może być kwestia braku zdefiniowania odpowiedniego albumu
    # ImageForm zamiast fileField?
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        # model = ImageAlbum   # tego nie było / old
        model = Image   # new
        fields = EntryForm.Meta.fields + ['images',]
