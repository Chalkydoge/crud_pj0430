from backend.models import Course, Comment, Teacher, MakeComment, Department
from backend.serializer import CourseSerializer, CommentSerializer, UserSerializer, MakeCommentSerializer
from backend.permissions import IsOwnerOrReadOnly, HasPermToWrite, HasPermToEditAndDelete, IsSuperUserOrAuthenticatedOrReadOnly

from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User, Permission
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
		'make_comment': reverse('make_comment-list', request=request, format=format)
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
		if 'c_teacher_name' in q_fields:
			q_teacher = self.request.GET['c_teacher_name']
			possible_teachers = Teacher.objects.filter(t_name__contains=q_teacher)
			ans_queryset = ans_queryset.filter(c_teacher__in=possible_teachers)
		# 课程名称的过滤(包含字段)
		if 'c_name' in q_fields:
			q_name = self.request.GET['c_name']
			ans_queryset = ans_queryset.filter(c_name__contains=q_name)
		# 上课地点的过滤
		if 'c_classroom' in q_fields:
			q_classroom = self.request.GET['c_classroom']
			ans_queryset = ans_queryset.filter(c_classroom__contains=q_classroom)
		# 课程号的过滤
		if 'c_id' in q_fields:
			q_id = self.request.GET['c_id']
			ans_queryset = ans_queryset.filter(c_id__contains=q_id)
		# 开课院系的过滤
		if 'c_dept_name' in q_fields:
			q_dept = self.request.GET['c_dept_name']
			possible_depts = Department.objects.filter(d_name__contains=q_dept)
			ans_queryset = ans_queryset.filter(c_dept__in=possible_depts)
		return ans_queryset

	# def list(self, request):
	# 	queryset = self.get_queryset()
	# 	serializer = CourseSerializer(queryset, many=True)
	# 	return Response(serializer.data)

	def perform_create(self, serializer):
		print(self.request.data)
		input_id = self.request.data['c_id']
		input_name = self.request.data['c_name']
		input_classroom = self.request.data['c_classroom']
		input_teacher = self.request.data['c_teacher_name']
		input_teacher_dept = self.request.data['c_tdept_name']
		input_dept = self.request.data['c_dept_name']

		teacher_dept = Department.objects.get_or_create(d_name=input_teacher_dept)[0]
		teacher = Teacher.objects.get_or_create(t_name=input_teacher, t_dept=teacher_dept)[0] #
		course_dept = Department.objects.get_or_create(d_name=input_dept)[0]
		course = Course.objects.get_or_create(c_id=input_id, c_name=input_name, c_teacher=teacher, c_classroom=input_classroom, c_dept=course_dept)
		print("Created!!!")

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	获取, 更新或是删除某一门课程的信息
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_update(self, serializer):
		input_id = self.request.data['c_id']
		input_name = self.request.data['c_name']
		input_classroom = self.request.data['c_classroom']
		input_teacher = self.request.data['c_teacher_name']
		input_teacher_dept = self.request.data['c_tdept_name']
		input_dept = self.request.data['c_dept_name']
		teacher_dept = Department.objects.get_or_create(d_name=input_teacher_dept)[0]
		teacher = Teacher.objects.get_or_create(t_name=input_teacher, t_dept=teacher_dept)[0] #
		course_dept = Department.objects.get_or_create(d_name=input_dept)[0]

		obj = serializer.save(c_id=input_id, c_name=input_name, c_teacher=teacher, c_dept=course_dept, c_classroom=input_classroom)
		print(obj)
		print("Success!!!")
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
		print(self.request.data)
		q_cid = self.request.data['p_cid']
		q_rate = self.request.data['p_rate']
		q_comment = self.request.data['p_comment']
		q_owner = self.request.data['p_owner']
		course = Course.objects.get(c_id=q_cid)
		obj = serializer.save(p_cid=course, p_rate=q_rate, p_comment=q_comment)
		self.check_object_permissions(self.request, obj)
		if q_owner is not None:
			u = User.objects.get(username=q_owner)
			m = MakeComment.objects.create(m_commentid=obj, m_owner=u)
		print("Created Successfully!")

	# 定义一个自定义查询评论的视图函数
	def get_queryset(self):
		q_fields = self.request.GET.keys()
		ans_queryset = Comment.objects.all()
		if 'p_cid' in q_fields:
			q_cid = self.request.GET['p_cid']
			possible_courses = Course.objects.filter(c_id__contains=q_cid)
			ans_queryset = ans_queryset.filter(p_cid__in=possible_courses)
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
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	def get_queryset(self):
		ans_queryset = User.objects.all()
		q_fields = self.request.GET.keys()
		if 'username' in q_fields:
			ans_queryset = ans_queryset.filter(username=self.request.GET['username'])
		return ans_queryset

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsSuperUserOrAuthenticatedOrReadOnly]
	def perform_update(self, serializer):
		print(self.request.data)
		q_username = self.request.data['username']
		q_password = self.request.data['password']
		q_perm = self.request.data['perm']
		q_id = self.request.data['id']
		target_user = User.objects.get(pk=q_id)
		print(target_user.has_perm('backend.add_comment'))
		not_blocked = target_user.has_perm('backend.add_comment')
		if q_perm == 'blocked' and not_blocked: # 没有被封禁的才可以被移除权限
			temp = Permission.objects.get(name='Can add comment')
			target_user.user_permissions.remove(temp)	
		if q_perm == 'unblocked' and not_blocked == False: # 只有已经被封禁的才可以被解封
			temp = Permission.objects.get(name='Can add comment')
			target_user.user_permissions.add(temp)
		obj = serializer.save(username=q_username, password=q_password)
		print("After: ", target_user.has_perm('backend.add_comment'))

class MakeCommentList(generics.ListCreateAPIView):
	queryset = MakeComment.objects.all()
	serializer_class = MakeCommentSerializer
	def get_queryset(self):
		ans_queryset = MakeComment.objects.all()
		q_fields = self.request.GET.keys()
		if 'm_commentid' in q_fields:
			ans_queryset = ans_queryset.filter(m_commentid=self.request.GET['m_commentid'])
		return ans_queryset