import re
from rest_framework import serializers
from .models import Course, Comment, Teacher, Department
from django.contrib.auth.models import User, Permission

# 写一个序列化器, 处理拿到的数据
class CourseSerializer(serializers.ModelSerializer):
	"""
	课程信息的序列化器, 将API响应的数据序列化为json/dict格式
	需要增加验证的功能(比如添加新的课程信息必须有效)
	"""
	c_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
	c_dept = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
	
	def validate_c_id(self, value):
		"""
		验证课程号是否合法 eg: XXX1100010.ss 就是不合法的编码
		4位的院系编码 + 6位的课程代码(2位标识(11/12/13)+4位序号) + '.' + 课程号码(一门课程由多位老师开设)
		"""
		pattern = re.compile(r'([A-Z]{4})({11|12|13})([0-9]{4}).([0-9]{2})')
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
		fields = ['c_id', 'c_name', 'c_teacher', 'c_classroom', 'c_dept']

# Comments: 用户对于课程的评价信息
class CommentSerializer(serializers.ModelSerializer):
	"""
	用户评论的序列化器
	"""
	p_owner = serializers.ReadOnlyField(source='p_owner.username')
	class Meta:
		model = Comment
		fields = ['p_id', 'p_cid', 'p_rate', 'p_comment', 'p_owner',]

class UserSerializer(serializers.ModelSerializer):
	# comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
	def create(self, validated_data):
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
		fields = ['id', 'username', 'password', 'is_superuser']