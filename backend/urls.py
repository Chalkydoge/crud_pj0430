from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views

router = DefaultRouter()
# register: API的名字 + 相应的视图集合
# router.register('show_orgs', views.OrgViewSet)

# API的路由设置
urlpatterns = [
	path('', views.api_root),
	path('courses/', views.CourseList.as_view(), name='courses-list'),
	path('courses/<str:pk>/', views.CourseDetail.as_view(), name='courses-detail'),
	#
	path('users/', views.UserList.as_view(), name='user-list'),
	path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
	#
	path('comments/', views.CommentList.as_view(), name='comments-list'),
	path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comments-detail'),
	#
	path('make_comment/', views.MakeCommentList.as_view(), name='make_comment-list'),
	#
	path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)