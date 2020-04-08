from django.urls import path
from django.conf.urls import url
from .views import (
    ProductListView, 
    #product_list_view,
    #ProductDetailView,
    #product_detail_view,
    #ProductFeaturedListView,
    #ProductFeaturedDetailView,
    ProductDetailSlugView,
    )

urlpatterns = [
   
    url(r'^$', ProductListView.as_view(), name='list'),
    # url(r'^productnew/$', product_list_view),

    # url(r'^featured/$', ProductFeaturedListView.as_view()),
    # url(r'^featured/(?P<pk>\d+)$', ProductFeaturedDetailView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    # url(r'^product/(?P<pk>\d+)/$',  ProductDetailView.as_view()),
    # url(r'^productnew/(?P<pk>\d+)/$', product_detail_view),
]
