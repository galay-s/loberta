from django.urls import path
from links import views

urlpatterns = [
    path(r'', views.links, name='links'),
    path(r'<int:link_id>', views.up_down_link, name='up_down_link'),
    path(
        r'get_links_statuses',
        views.get_links_statuses,
        name='get_links_statuses'),
]
