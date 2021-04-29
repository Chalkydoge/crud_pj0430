# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Department(models.Model):
	d_id = models.AutoField(primary_key=True)
	d_name = models.CharField(max_length=20)

	def __str__(self):
		return self.d_name

class Teacher(models.Model):
	t_id = models.AutoField(primary_key=True)
	t_name = models.CharField(max_length=10)
	t_dept = models.ForeignKey(Department, on_delete=models.CASCADE)

	def __str__(self):
		return self.t_name

class Course(models.Model):
	c_id = models.CharField(max_length=20, primary_key=True) # eg: COMP130135.01
	c_name = models.CharField(max_length=20) # 面向对象程序设计
	c_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) # 刘卉
	c_classroom = models.CharField(max_length=10) # eg: H4201
	c_dept = models.ForeignKey(Department, on_delete=models.CASCADE)

	def __str__(self):
		return self.c_id

class Comment(models.Model):
	p_id = models.AutoField(primary_key=True)
	p_cid = models.ForeignKey(Course, on_delete=models.CASCADE)
	p_rate = models.IntegerField(validators=[
		MinValueValidator(0),
		MaxValueValidator(100)
	])
	p_comment = models.CharField(max_length=200)

class MakeComment(models.Model):
	m_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	m_commentid = models.OneToOneField(Comment, on_delete=models.CASCADE)

class BadComment(models.Model):
	b_owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	b_count = models.IntegerField()


# A Snippet for database creations
# $ python manage.py shell
# from backend.models import Course, Teacher, Department
# td = Department(d_name="软件学院")
# td = Department(d_name="信息科学与工程学院")
# td = Department(d_name="计算机科学技术学院")
# Department.objects.all()


# t = Department.objects.get(d_name="计算机科学技术学院")
# tt = Teacher(t_name="赵一鸣", t_dept=t)
# tt = Teacher(t_name="周雅倩", t_dept=t)
# tt = Teacher(t_name="刘卉", t_dept=t)
# Teacher.objects.all()

# tt = Teacher.objects.get(t_name="刘卉")
# tt = Teacher.objects.get(t_name="赵一鸣")
# tc = Course(c_id="COMP130135.03", c_name="面向对象程序设计", c_teacher=tt, c_classroom="H4204", c_dept=td)
# tc = Course(c_id="COMP130135.01", c_name="面向对象程序设计", c_teacher=tt, c_classroom="H4203", c_dept=td)
# tc = Course(c_id="COMP130005.01", c_name="代数逻辑与数理结构", c_teacher=tt, c_classroom="H3106", c_dept=td)
# Course.objects.all()