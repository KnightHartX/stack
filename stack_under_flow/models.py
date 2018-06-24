from django.db import models
from django.contrib.auth.models import AbstractUser


# 备忘：数据库更新命令：
# $ python manage.py makemigrations
# $ python manage.py migrate

# Question：
# ID(int自增）
# Title（varchar）
# Content（varchar）
# User.ID(int)
# answercount(int)
# up(int)
# down(int)
# display(bool)
# view(int)

# 下面的还没做
# tagjavascript(bool)
# tagcpp(bool)

# 问题的模型
class question(models.Model):
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=5000)
    contentstring=models.CharField(max_length=5000)
    userid = models.IntegerField(default=114514)
    useridnickname = models.CharField(max_length=50)
    answercount = models.IntegerField(default=0)
    display = models.BooleanField(default=1)
    view = models.IntegerField(default=0)
    update_time = models.DateTimeField('发布时间', auto_now_add=True)
    giftpoint=models.IntegerField(default=0)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题'
# 回答的模型
class answer(models.Model):
    content = models.CharField(max_length=5000)
    contentstring=models.CharField(max_length=5000)
    userid = models.IntegerField(default=114514)
    questionid= models.IntegerField(default=114514)
    loushu=models.IntegerField(default=1)
    useridnickname = models.CharField(max_length=50)
    display = models.BooleanField(default=1)
    update_time = models.DateTimeField('发布时间', auto_now_add=True)

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = '回答'

class tag(models.Model):
    tagname=models.CharField(max_length=500)
    qcountintag=models.IntegerField(default=0)
    questions=models.ManyToManyField(question,related_name='tag_questions')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    # 手动命令行建立联系
    # from stack_under_flow.models import question, tag
    # a = question.objects.get(id=2)
    # b = tag.objects.get(id=2)
    # a.tag_questions.add(b)

class message(models.Model):
    sendmessage_usernickname=models.CharField(max_length=500)
    receivemessage_usernickname=models.CharField(max_length=500)
    message_content=models.CharField(max_length=5000)
    message_sendtime=models.DateTimeField('发送时间', auto_now_add=True)
    message_questionid=models.IntegerField(default=0)
    message_status=models.CharField(default='unread',max_length=500)
    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'