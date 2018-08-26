from django.conf.urls import url

from alfa import views

urlpatterns = [
	url(r'^$', views.home_page, name='home_url'),
	url(r'^admin/$', views.admin_page, name='admin_url'),
	url(r'^login/$', views.login_page, name='login_url'),
	url(r'^registration/$', views.reg_page, name='reg_url'),
	url(r'^forgot_password/$', views.forgot_password_page, name='forgot_password_url'),
	url(r'^logout/$', views.logout_page, name='logout_url'),
	url(r'^article/new/$', views.edit_article_page, name='new_article_url'),
	url(r'^article/edit/(?P<id>\d+)$', views.edit_article_page, name='edit_article_url'),
	url(r'^article/remove/(?P<id>\d+)$', views.remove_article_page, name='remove_article_url'),
	url(r'^article/(?P<id>\d+)$', views.article_page, name='article_url'),
]
