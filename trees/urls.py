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
    path('entry/<int:pk>/remove', views.TreeDeleteEntry.as_view(), name='delete_entry'),
    path('entry/edit/<int:pk>', views.TreeEditEntry.as_view(), name='edit_entry'),
    path('image_album/<int:pk>/remove', views.TreeDeleteImageAlbum.as_view(), name='delete_image_album'),
    path('new_tree/', views.NewTree.as_view(), name='new_tree'),
    # path('user_trees/<', views.UserTrees.as_view(), name='user_trees'),
    path('user_trees/<int:pk>/', views.UserTrees.as_view(), name='user_trees'),

    path('tree/<int:pk>/', views.TreeView.as_view(), name='tree'),  # old
    path('tree/<int:pk>/edit_tree', views.EditTree.as_view(), name='edit_tree'),
    path('tree/<int:pk>/delete_tree', views.DeleteTree.as_view(), name='delete_tree'),
    # path('tree/<int:pk>/', views.TreeDislpayEntries.as_view(), name='tree'),   # new

    # path('tree/<int:tree_id>/', views.tree, name='tree'),
    # path('new_entry/', views.new_entry, name='new_entry'),
    # path('entry/<int:entry_id>/', views.entry, name='entry'),

    path('new_test_tree/', views.NewTestTree.as_view(), name='new_test_tree'),
    # temporary, test:
    # path('signup/', views.SignUpView.as_view(), name='signup'),

]

if settings.DEBUG:          # if not needed?
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)