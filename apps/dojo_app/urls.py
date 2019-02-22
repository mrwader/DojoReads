from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.display_books),
    url(r'^add_book_page$', views.add_book_page),
    url(r'^add_book$', views.add_book),
    url(r'^add_author$', views.add_author),
    url(r'^books/(?P<id>\d+)$', views.view_book),
    url(r'^add_review$', views.add_review),
    url(r'^users/(?P<id>\d+)$', views.view_user),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review),
]