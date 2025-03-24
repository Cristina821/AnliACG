from django.urls import path,re_path
from . import views
urlpatterns=[
	path('',views.jump,name="jump"),

	path('users',views.indexUsers,name="indexusers"),
	path('users/add',views.addUsers,name="addusers"),
	path('users/insert',views.insertUsers,name="insertusers"),
	path('users/del/<int:uid>',views.delUsers,name="delusers"),
	path('users/loginpage',views.loginpage,name="loginpage"),
	path('users/logoutpage',views.logoutpage,name="logoutpage"),
	path('users/menu',views.menu,name="menu"),

	path('animate/manage',views.animate_manage,name="animanage"),
	path('animate/update',views.animate_update,name="aniupdate"),
	path('animate/del/<int:aid>',views.animate_delete,name="anidelete"),
	path('animate/delall',views.animate_delall,name="anidelall"),
	path('animate/search',views.animate_search,name="anisearch"),

	path('article',views.article_homepage,name="arthomepage"),
	path('article/writing',views.article_writing,name="artwriting"),
	path('article/insert',views.article_insert,name="artinsert"),
	re_path('article_detail/(\d)/',views.article_detail),
	path('article/comment/insert',views.artcommon_insert,name="artcominsert"),
	path('article/target_check',views.target_check,name="comtarcheck")
]