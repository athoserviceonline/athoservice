'''

# Shell session 1
# python manage.py shell

'''

from tags.models import Tag 

qs = Tag.objects.all()
print(qs)
black = Tag.objects.last()

black.title
black.slug

black.products

'''

returns:
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager, <locals>, ManyRelatedMany

'''
from products.models import products

qs = Product.objects.all()
print(qs)
tshirt= qs.first()
tshirt.title
tshirt.description

tshirt.tag

'''
Raises an error because the Product model doesnot have
a field "tag"
'''

tshirt.tags
'''
Raises an error because the Product model doesnot have a field "tags"
'''

tshirt.tag_set

tshirt.tag_set.all()

'''
Return an actual Queryset of the Tag
model related to this product
<QuerySet [<Tag: T shirt>, <Tag: TShirt>,<Tag: T-shirt>, <Tag: Red>, <Tag: Black>]>
'''

tshirt.tag_set.all()

tshirt.tag_set.filter(title__icontains='black')