from django.shortcuts import render
from django.views.generic import ListView

from shopping.models import Product


class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		context['query'] = self.request.GET.get('q')
		#SearchQuery.objects.create(query=query)
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		method_dict = request.GET
		query= method_dict.get('q', None)
		print(query)
		if query is not None:			
			return Product.objects.search(query)
		
		return Product.objects.featured()		



#

'''

__icontains = field contains this
__iexact 	= fields is exactly this


if query is not None:
			lookups = Q(title__icontains=query) | Q(description__icontains=query)
			return Product.objects.filter(lookups).distinct()
		return Product.objects.featured()	

'''