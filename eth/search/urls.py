from django.urls import path
from django.conf.urls import url
# from shopping.views import (
#     ProductListView,
#     )
from search.views import (
    SearchProductView,
    )


urlpatterns = [
   
    url(r'^$', SearchProductView.as_view(), name='query'),

]
