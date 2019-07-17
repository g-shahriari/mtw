from django.conf.urls import url
from first_app import views

urlpatterns = [
    url(r'^$',views.BaseView.as_view(),name='post_list'),
    # url(r'^$', views.qet_queryset, name='test'),
    url(r'^query (?P<num>[0-9]+)/$', views.qet_queryset,name='query'),

    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^test/$', views.my_custom_sql, name='test'),
    # url(r'^createnewcustomer/$', views.CreateNewCustomer.as_view(), name='createnewcustomer'),

    url(r'^proflie/$', views.ProfileView.as_view(), name='profile'),

    # url(r'^store (?P<id>[0-9]+)$', views.qet_queryse,name='store'),
    url(r'^createnewcustomer/$',views.customer_register,name='customer'),
    url(r'^createnewseller/$',views.seller_register,name='seller'),
    url(r'^poll/$',views.poll,name='poll'),
    url(r'^quer (?P<num>[0-9]+)/$', views.similarity_list_based_search_by_search_check,name='sim_search_by_search'),
]
