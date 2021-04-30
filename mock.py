import os
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_project.settings')

import django
django.setup()

from backend.models import Course, Teacher, Department, Comment, BadComment
from django.contrib.auth.models import User
prob_depts = [('MATH', '数学科学学院'), ('CHIN','中国语言文学系'), ('PHIL', '哲学学院'), ('ECON', '经济学院'),
	('PHYS', '物理学系'), ('COMP', '计算机科学技术学院'), ('SOFT', '软件学院'), ('INFO', '信息科学与工程学院'),
	('MACR', '高分子科学系'), ('MICR', '微电子学院'), ('BIOL', '生命科学学院'), ('ENVI', '环境科学与工程系'),
]

prob_tname = ['戴燕', '周双全', '段怀清', '聂安福', '侯健', '汪卫', '危辉', '吴晓峰', '艾剑良', '施郁',
	'蒋平', '董骁', '董文博', '郭志刚', '刘学礼', '赵琳', '陈莉萍', '白建松', '宋颖', '易婷', '蒋玉龙',
	'张卫', '任俊彦', '管箫', '阚海斌', '阚海国', '阚建斌', '张建斌', '周水庚', '何震瀛', '唐志强', 
	'孙未未', '陈雁秋', '冯辉', '秦亚杰', '徐蔚', '陈睿', '他得安', '徐丰', '解玉凤'
]

prob_cname = ['数字逻辑基础', '机器学习', '集合与图论', '数据库引论', '数据库论引', '据库论引数', '论引数据库', '引数据库论',
	'学习机器', '数据结构', '结构数据', '抽象代数', '计算机与互联网的未来', '营销创新', '航空航天技术发展导论', '智能可穿戴材料导论',
	'应用伦理学', '中国近现代史纲要', '当代世界经济与政治', '宋词导读', '中国现代文学名著选讲', '西方道德哲学原著选读', '经济与社会'
	'计算思维', '思维计算'
]

prob_cid_type = ['11', '12', '13']

prob_building = ['H2', 'H3', 'H4', 'H5', 'H6', 'HGX', 'HGD', 'F', 'JA', 'JB', 'Z']

NUM_OF_COURSES = 30

NUM_OF_COMMENTS = 50

NUM_OF_DEPTS = len(prob_depts)

NUM_OF_BUILDINGS = len(prob_building)

NUM_OF_TEACHERS = len(prob_tname)

NUM_OF_CNAME = len(prob_cname)

def rand_classroom():
	classroom = ''.join(random.sample(string.digits, 3))
	p = random.randint(0, NUM_OF_BUILDINGS - 1)
	build = prob_building[p]
	return build + classroom


for i in range(NUM_OF_COURSES):
	dept_pick = random.randint(0, NUM_OF_DEPTS - 1)
	dept = prob_depts[dept_pick] # 目标院系元组
	head = prob_cid_type[random.randint(0, 2)]
	body = ''.join(random.sample(string.digits, 4))
	tail = ''.join(random.sample(string.digits, 2))
	mock_cid = dept[0] + head + body + '.' + tail
	mock_cdept = dept[1]
	mock_cclassroom = rand_classroom()
	mock_cteacher = prob_tname[random.randint(0, NUM_OF_TEACHERS - 1)]
	mock_cname = prob_cname[random.randint(0, NUM_OF_CNAME - 1)]
	# print(mock_cid, mock_cteacher, mock_cname, mock_cdept, mock_cclassroom)

	td = Department.objects.get_or_create(d_name=mock_cdept) 
	t = Teacher.objects.get_or_create(t_name=mock_cteacher, t_dept=td[0])
	tc = Course.objects.get_or_create(c_id=mock_cid, c_name=mock_cname,
		c_teacher=t[0], c_classroom=mock_cclassroom, c_dept=td[0])
