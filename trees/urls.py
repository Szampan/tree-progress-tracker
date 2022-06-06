from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'trees'
urlpatterns = [
    # path('', views.index, name='index'),              # function-based view
    path('', views.Index.as_view(), name='index'),      # Class-based view
    path('all_entries/', views.AllEntries.as_view(), name='all_entries'),             
    path('entry/<int:pk>/', views.EntryView.as_view(), name='entry'),             
    path('tree/<int:pk>/', views.TreeView.as_view(), name='tree'),              

    # path('tree/<int:tree_id>/', views.tree, name='tree'),
    # path('new_entry/', views.new_entry, name='new_entry'),
    # path('entry/<int:entry_id>/', views.entry, name='entry'),

]

if settings.DEBUG:          # if not needed?
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)