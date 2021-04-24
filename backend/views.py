from backend.models import Course, Comment, Teacher
from backend.serializer import CourseSerializer, CommentSerializer, UserSerializer
from backend.permissions import IsOwnerOrReadOnly, HasPermToWrite, HasPermToEditAndDelete

from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'courses': reverse('courses-list', request=request, format=format),
		'comments': reverse('comments-list', request=request, format=format),
		})

class CourseList(generics.ListCreateAPIView):
	"""
	列出所有的课程信息/新建一个课程信息
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		# print(self.request.GET)
		q_fields = self.request.GET.keys()
		ans_queryset = Course.objects.all()
		# 授课教师的过滤(包含课程教师名称)
		if 'c_teacher' in q_fields:
			q_teacher = self.request.GET['c_teacher']
			possible_teachers = Teacher.objects.filter(t_name__contains=q_teacher)
			ans_queryset = ans_queryset.filter(c_teacher__in=possible_teachers)
		# 课程名称的过滤(包含字段)
		if 'c_name' in q_fields:
			q_name = self.request.GET['c_name']
			ans_queryset = ans_queryset.filter(c_name__contains=q_name)

		return ans_queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CourseSerializer(queryset, many=True)
		return Response(serializer.data)

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	获取, 更新或是删除某一门课程的信息
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentList(generics.ListCreateAPIView):
	"""
	Lists(GET), Create(POST)
	展示所有的评课信息, 同时允许登录用户增加课评
	"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly & HasPermToWrite]
	# TODO perform create from post(by frontend)
	def perform_create(self, serializer):
		obj = serializer.save(p_owner=self.request.user)
		self.check_object_permissions(self.request, obj)
	# TODO
	def get_queryset(self):
		q_fields = self.request.GET.keys()
		ans_queryset = Comment.objects.all()
		if 'p_cid' in q_fields:
			q_cid = self.request.GET['p_cid']
			possible_courses = Course.objects.filter(c_id__contains=q_cid)
			ans_queryset = ans_queryset.filter(p_cid__in=possible_courses)
		if 'p_owner' in q_fields:
			q_owner = self.request.GET['p_owner']
			ans_queryset = ans_queryset.filter(p_owner__username=p_owner)
		return ans_queryset

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve(GET), Update(PUT), Destroy(DELETE)
	获取课评, 更新课评, 删除课评的页面
	"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, HasPermToEditAndDelete]

	def perform_update(self, serializer):
		q_rate = self.request.data['p_rate']
		q_comment = self.request.data['p_comment']
		obj = serializer.save(p_rate=q_rate, p_comment=q_comment)
		self.check_object_permissions(self.request, obj)

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	def get_queryset(self):
		ans_queryset = User.objects.all()
		q_fields = self.request.GET.keys()
		if 'username' in q_fields:
			ans_queryset = ans_queryset.filter(username=self.request.GET['username'])
		return ans_queryset

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer