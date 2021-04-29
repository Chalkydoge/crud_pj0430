import re
from rest_framework import serializers
from .models import Course, Comment, Teacher, Department, MakeComment, BadComment
from django.contrib.auth.models import User, Permission

# 写一个序列化器, 处理拿到的数据
class CourseSerializer(serializers.ModelSerializer):
	"""
	课程信息的序列化器, 将API响应的数据序列化为json/dict格式
	需要增加验证的功能(比如添加新的课程信息必须有效)
	"""
	c_teacher_name = serializers.ReadOnlyField(source="c_teacher.t_name")
	c_dept_name = serializers.ReadOnlyField(source="c_dept.d_name")
	
	def validate_c_id(self, value):
		"""
		验证课程号是否合法 eg: XXX1100010.ss 就是不合法的编码
		4位的院系编码 + 6位的课程代码(2位标识(11/12/13)+4位序号) + '.' + 课程号码(一门课程由多位老师开设)
		"""
		pattern = re.compile(r'[A-Z]{4}(11|12|13)[0-9]{3,4}\.[0-9]{2}$')
		if re.match(pattern, value) is None:
			raise serializers.ValidationError("课程号格式错误!")
		return value

	def validate_c_classroom(self, value):
		"""
		验证以下上课地点是不是乱填的
		只有以下开头的地点才是有效的: H, HQ, HGD, HGX, F, Z, J

		"""
		pattern = re.compile(r'((H)|(HGD)|(HGX)|(F)|(Z)|(JA)|(JB))([0-9]{3,4})(A|B|\b)$')
		if re.match(pattern, value) is None:
			raise serializers.ValidationError("教室编号格式错误!")
		return value

	class Meta:
		model = Course
		fields = ['c_id', 'c_name', 'c_teacher_name', 'c_classroom', 'c_dept_name']

# Comments: 用户对于课程的评价信息
class CommentSerializer(serializers.ModelSerializer):
	"""
	用户评论的序列化器
	"""
	p_coursename = serializers.ReadOnlyField(source="p_cid.c_name")
	class Meta:
		model = Comment
		fields = ['p_id', 'p_cid', 'p_rate', 'p_comment', 'p_coursename']

class UserSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		print("Call here")
		username = validated_data['username']
		password = validated_data['password']
		u = User.objects.create_user(username=username, password=password)
		initial_perm_list = ['Can add comment', 'Can view comment', 'Can change comment', 'Can delete comment']
		for perm in initial_perm_list:
			p = Permission.objects.get(name=perm)
			u.user_permissions.add(p)
		return u

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'is_superuser', 'email']

class MakeCommentSerializer(serializers.ModelSerializer):
	m_username = serializers.ReadOnlyField(source="m_owner.username")
	class Meta:
		model = MakeComment
		fields = ['m_owner', 'm_commentid', 'm_username']

class BadCommentSerializer(serializers.ModelSerializer):
	b_username = serializers.ReadOnlyField(source='b_owner.username')
	class Meta:
		model = BadComment
		fields = ['b_owner', 'b_count', 'b_username']