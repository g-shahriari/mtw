from django.conf.urls import url
from first_app import views

urlpatterns = [
    url(r'^$',views.BaseView.as_view(),name='post_list'),
    # url(r'^$', views.qet_queryset, name='test'),
    url(r'^query (?P<num>[0-9]+)/$', views.qet_queryset,name='query'),

    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^test/$', views.my_custom_sql, name='test'),
    url(r'^createnewcustomer/$', views.CreateNewCustomer.as_view(), name='createnewcustomer'),
    url(r'^createnewseller/$', views.CreateNewSeller.as_view(), name='createnewseller'),


]
