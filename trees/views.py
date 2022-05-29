from re import T
from django.shortcuts import render


from .models import Tree, Entry

def index(request):
    # trees = Tree.objects.all()
    trees = Tree.objects.order_by('date_added')
    context = {'trees': trees}
    return render(request, 'trees/index.html', context)

def tree(request, tree_id):
    tree = Tree.objects.get(id=tree_id)
    entries = tree.entry_set.order_by('date_added')
    context = {'tree': tree, 'entries': entries}
    return render(request, 'trees/tree.html', context)