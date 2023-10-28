from django.urls import path

from blogpost.apps import BlogpostConfig
from blogpost.views import BlogpostListView, BlogpostDetailView
from django.views.decorators.cache import cache_page

app_name = BlogpostConfig.name


urlpatterns = [
    path('', BlogpostListView.as_view(), name='blogpost_list'),
    path('view/<int:pk>', cache_page(60)(BlogpostDetailView.as_view()), name='view'),
]