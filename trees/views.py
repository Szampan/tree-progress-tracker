from django.shortcuts import render

from trees.forms import EntryFullForm
##
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
##
# from django.forms import modelformset_factory
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import HttpResponseRedirect
# from .forms import TreeForm, EntryForm, ImageForm
##
from .models import Tree, Entry, Images
from .forms import TreeForm

class Index(ListView):
    model = Tree
    template_name = 'trees/index.html'
    context_object_name = 'trees'   # default: object_list

    # def post(self, request, *args, **kwargs):
    #     form = EntryFullForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse_lazy('trees:index', kwargs={'pk': 'pk'}))
    #     context = self.get_context_data(object_list=self.get_queryset())
    #     return self.render_to_response(context)
    
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)

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

class TreeView(ListView):
    model = Entry
    template_name = 'trees/tree.html'
    context_object_name = 'tree_entries'
    # paginate_by = 10
    def get_queryset(self, *args, **kwargs):
        # return Tree.objects.filter(tree_id=self.kwargs['pk'])
        qs = super(TreeView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(tree_id=self.kwargs['pk'])
        return qs
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tree_name'] = Tree.objects.get(pk=self.kwargs['pk'])
        return context


class EntryView(DetailView):
    model = Entry
    template_name = 'trees/entry.html'
    context_object_name = 'entry'


class NewTree(FormView):
    form_class = TreeForm
    template_name = 'trees/new_tree.html'
    success_url = reverse_lazy('trees:index')




# def index(request):
#     # trees = Tree.objects.all()
#     trees = Tree.objects.order_by('date_added')
#     context = {'trees': trees}
#     return render(request, 'trees/index.html', context)

# def tree(request, tree_id):
#     tree = Tree.objects.get(id=tree_id)
#     entries = tree.entry_set.order_by('date_added')
#     context = {'tree': tree, 'entries': entries}
#     return render(request, 'trees/tree.html', context)

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
