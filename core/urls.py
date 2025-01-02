from core import views
from django.urls import path

urlpatterns = [
    path("",views.index,name='index'),
    path("form",views.register_form,name='register_form'),
    path("login",views.user_login,name='user_login'),
    path("signup",views.user_register,name='user_register'),
    path("logout",views.user_logout,name='user_logout'),
]


urlpatterns+=[
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsevents/', views.newsevents, name='newsevents'),

    # BLOGS
    path('blog/commitie/', views.commitie, name='commitie'),
    path('blog/gallery/', views.gallery, name='gallery'),
    path('blog/vgallery/', views.vgallery, name='vgallery'),
    path('blog/privacy-policy/', views.pp, name='privacy_policy'),
    path('blog/terms-and-conditions/', views.tc, name='terms_conditions'),
    
    # Individual Blog Posts
    path('blog/ispl-player-revealed/', views.b1, name='ispl_player_revealed'),
    path('blog/own-a-tspl-franchise-team/', views.b2, name='own_tspl_franchise'),
    path('blog/tennies-ball-cricket/', views.b3, name='tennies_ball_cricket'),
    path('blog/tspl-t10-action/', views.b4, name='tspl_t10_action'),
    path('blog/who-can-register/', views.b5, name='who_can_register'),
]