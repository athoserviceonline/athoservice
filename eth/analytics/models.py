from django.conf import settings
from django.http import Http404

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session 

from django.db import models
from django.db.models.signals import pre_save, post_save

from accounts.signals import user_logged_in
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) # User instance instance.id
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True) # User, Product, Order, Cart, Address
    object_id       = models.PositiveIntegerField() #User id, Product id, Order id,
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_object  = GenericForeignKey('content_type', 'object_id') # Product Instance
    timestamp       = models.DateTimeField(auto_now_add=True)

    # product 		= models.ForeignKey(Product) # id = 1, product_obj.objectviewed_set.all()
    # order 		= models.ForeignKey(Order)
    #url

    def __str__(self, ):
        return "%s viewed on: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
        c_type = ContentType.objects.get_for_model(sender) #instance.__class__
        # print(sender)
        # print(instance)
        # print(request)
        # print(request.user)
        try:
            new_view_obj = ObjectViewed.objects.create(
                user = request.user,
                content_type =c_type,
                object_id = instance.id,
                ip_address = get_client_ip(request)
                )
        except ValueError as exception:
            new_view_obj = ObjectViewed.objects.create(
                user = None,
                content_type =c_type,
                object_id = instance.id,
                ip_address = get_client_ip(request)
                )
        except:
             raise Http404("for Anonymous user product does not exist")

object_viewed_signal.connect(object_viewed_receiver)



class UserSession(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) # User instance instance.id
    ip_address      = models.CharField(max_length=220, blank=True, null=True) # IP Field
    session_key     = models.CharField(max_length=100, blank=True, null=True) # min 50
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended           = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


# def pre_save_session_receiver(sender, instance, created, *args, **kwargs):


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id) 
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id) 
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    #print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key= request.session.session_key # having different in their versions
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key= session_key
        )

user_logged_in.connect(user_logged_in_receiver)          
