from email.policy import default
from urllib import request
from django.shortcuts import render

##
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic import DeleteView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
##
# from django.forms import modelformset_factory
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import HttpResponseRedirect
# from .forms import TreeForm, EntryForm, ImageForm
##
from .models import Tree, Entry, Image, ImageAlbum
from .forms import TreeForm, EntryForm, FullEntryForm

from tools import *


class Index(ListView):
    model = Tree
    template_name = 'trees/index.html'
    context_object_name = 'trees'   # default: object_list

    def get_queryset(self, *args, **kwargs):
        qs = super(Index, self).get_queryset(*args, **kwargs)
        qs = qs.order_by('-date_added')
        return qs
        

class UserTrees(ListView):
    model = Tree
    template_name = 'trees/user_trees.html'
    context_object_name = 'user_trees'

    def get_queryset(self, *args, **kwargs):
        qs = super(UserTrees, self).get_queryset(*args, **kwargs)
        qs = qs.filter(owner_id=self.kwargs['pk'])
        # qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['owner_id'] = self.kwargs['pk']
        context['owner_name'] = User.objects.get(pk=self.kwargs['pk'])
        return context


class AllEntries(ListView):
    model = Entry
    template_name = 'trees/all_entries.html'
    context_object_name = 'all_entries'   


class TreeDislpayEntries(ListView):
    model = Entry
    template_name = 'trees/tree.html'
    context_object_name = 'tree_entries'
    
    def get_queryset(self, *args, **kwargs):
        # lol('▬▬▬ GET QUERYSET ▬▬▬')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tree_id=self.kwargs['pk'])
        qs = qs.order_by('-date_photos_taken', '-album_id')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tree_name'] = Tree.objects.get(pk=self.kwargs['pk'])   # zamiast tego można coś w stylu post.title w templacie
        # context['form'] = EntryForm()   # Old
        context['form'] = FullEntryForm()   # New
        return context

class TreeAddEntry(SingleObjectMixin, FormView):
    model = Tree
    form_class = EntryForm  # Old
    # form_class = FullEntryForm  # New; z tym nie działa - komunikat, "field is required" (mimo że wybrano)
    template_name = 'trees/tree.html'

    # problem: jeśli invalid, to wyświetla template ale bez entries

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()     # Tree object
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form): 
        entry = form.save(commit=False)
        entry.album = ImageAlbum.objects.create()
        entry.tree = self.object
        # lol(entry.__dict__)
        entry.save()

        files = self.request.FILES.getlist('images')
        default = True
        for file in files:
            Image.objects.create(album=entry.album, image=file, default=default)
            default = False
        return super().form_valid(form)

    def get_success_url(self):
        tree = self.get_object()
        return reverse('trees:tree', kwargs={'pk': tree.pk})


class TreeEditEntry(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'trees/edit_entry.html'

    def get_success_url(self):
        tree = self.object.tree
        return reverse('trees:tree', kwargs={'pk': tree.pk})
    
class TreeDeleteEntry(DeleteView):  # Add mixin to delete entry directly from a tree page
    model = Entry
    template_name = 'trees/delete_entry.html'  

    def get_success_url(self):
        tree = self.object.tree
        return reverse('trees:tree', kwargs={'pk': tree.pk})


class TreeDeleteImageAlbum(DeleteView):  # Add mixin to delete entry directly from a tree page
    model = ImageAlbum
    template_name = 'trees/delete_image_album.html'  

    # ! doesn't get the tree object
    def get_success_url(self):
        tree = ImageAlbum.objects.get(pk=self.object.pk)
        return reverse('trees:tree', kwargs={'pk': tree.pk})


class TreeView(View):

    def get(self, request, *args, **kwargs):
        view = TreeDislpayEntries.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TreeAddEntry.as_view()
        return view(request, *args, **kwargs)


class EntryView(DetailView):
    model = Entry
    template_name = 'trees/entry.html'
    context_object_name = 'entry'


class NewTree(FormView):
    form_class = TreeForm
    template_name = 'trees/new_tree.html'
    success_url = reverse_lazy('trees:index')

    def form_valid(self, form):
        new_tree = form.save(commit=False)
        new_tree.owner = self.request.user
        new_tree.save()

        return super().form_valid(form)


# @login_required
# def new_entry(request):
#     if request.method == 'POST':
#         # Images  will be in request.FILES
#         form = EntryFullForm(request.POST or None, request.FILES or None)
#         files = request.FILES.getlist('images')
#         if form.is_valid():











# @login_required
# def entry(request):

#     ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
#     if request.method == 'POST':
#         entry_form = EntryForm(request.POST)      
#         formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
#         if entry_form.is_valid() and formset.is_valid():
#             new_entry = entry_form.save(commit=False)   # commit=False -> don't save yet
#             new_entry.owner = request.user
#             # Add Tree here?
#             new_entry.save

#             for form in formset.cleaned_data:
#                 # this helps to not crash if the user do not upload all the photos
#                 if form:       
#                     image = form['image']
#                     photo = Images(post=new_entry, image=image)
#                     photo.save()
#             # use django messages framework
#             messages.success(request, 'Your entry has been created!')
#             return HttpResponseRedirect("/")
#         else:
#             print(entry_form.errors, formset.errors)
#     else:
#         entry_form = EntryForm()
#         formset = ImageFormSet(queryset=Images.objects.none())
#     return render(request, 'index.html', {'form': entry_form, 'formset': formset})    
