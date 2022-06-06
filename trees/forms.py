from django import forms
from .models import Tree, Entry, Images

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'specie', 'specie_latin', 'description', 'is_bonsai']

class EntryForm(forms.ModelForm):
    # Add tree here?
    text = forms.CharField(max_length=245, label="Description")       
    class Meta:
        model = Entry
        fields = ['text']

class EntryFullForm(EntryForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        fields = EntryForm.Meta.fields + ['images',]
               


# from django import forms
# from .models import Tree, Entry, Images


# class ImageForm(forms.ModelForm):
#     image = forms.ImageField(label="Image")
#     class Meta:
#         model = Images
#         fields = ('image', )