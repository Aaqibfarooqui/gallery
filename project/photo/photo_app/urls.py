from django.urls import path
from photo_app import views
from photo import settings
from django.conf.urls.static import static

urlpatterns=[
    path('index',views.index),
    path('about',views.about),
    path('contact',views.contact),
    # path('abc',views.abouts)
    path('services/<rid>',views.services),
    path('contact',views.contact),
    path('login',views.user_login),
    path('register',views.register),
    path('gallery',views.gallery),
    path('aqib',views.single),
    path('logout',views.user_logout),
    path('filter/<pid>',views.filter),
    path('sort/<sv>',views.sort),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remov),
    path('updateqty/<sv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment)
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
