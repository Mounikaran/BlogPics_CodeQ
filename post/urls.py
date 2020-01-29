from django.urls import path


from post import views

app_name = 'post'

urlpatterns = [
	path('', views.PostList.as_view(), name='postlist'),
	path('post/new-post/', views.UploadPost.as_view(), name='createpost'),
	path('post/<str:slug>/', views.PostDetail.as_view(), name='postdetail'),
	path('post/<str:slug>/delete', views.DeletePost.as_view(), name='delete'),

	path('post/<str:slug>/comment/',views.add_comment_to_post, name='comment'),
	path('post/<str:slug>/approve_comment/', views.comment_approve, name='approve_comment'),
	path('post/<int:pk>/remove_comment/', views.comment_remove, name='remove_comment'),
]
