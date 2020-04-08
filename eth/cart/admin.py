from django.contrib import admin

from .models import Cart


class CartAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'user']
	class Meta:
		model = Cart

# class CartProductAdmin(admin.ModelAdmin):
# 	list_display = ['__str__', 'products']
# 	class Meta:
# 		model = Cart
# class CartTotalAdmin(admin.ModelAdmin):
# 	list_display = ['__str__', 'total','products']
# 	class Meta:
# 		model = Cart
# class CartTimeAdmin(admin.ModelAdmin):
# 	list_display = ['__str__', 'updated']
# 	class Meta:
# 		model = Cart
admin.site.register(Cart, CartAdmin)

# admin.site.register(Cart)


