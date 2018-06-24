# Create your views here.

from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import *

from .models import *
from users.models import User
from django.contrib import messages
from markdown import markdown
from django.db.models import Q
from .htmltostring import strip_tags


def commitquestion(request):
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    if current_user.is_anonymous:
        messages.info(request, '请登录后再发表问题！')
        return HttpResponseRedirect('/')

    if request.method == "POST":
        try:

            title = request.POST["title"]
            content = markdown(request.POST["content"], extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
            giftpoint = request.POST["giftpoint"]
            print(title)
            print(content)
            print(giftpoint)
            int_giftpoint = int(giftpoint)
            if current_user.point < int_giftpoint:
                messages.info(request, '悬赏分数大于用户积分，请重新输入！')
                return HttpResponseRedirect('http://127.0.0.1:8000/stack_under_flow/commitquestion/')
            else:
                pass
            # 先增加相关问题信息
            questioncommit = question()
            questioncommit.title = title
            questioncommit.content = content
            questioncommit.contentstring = strip_tags(content)
            questioncommit.userid = current_user.id
            questioncommit.useridnickname = current_user.nickname
            questioncommit.giftpoint = int_giftpoint
            questioncommit.save()

            # 添加相关项目的标签(避免使用ajax的方法！)
            # a = questioncommit
            # alltags = tag.objects.all()
            # for item in alltags:
            #     if (request.POST[item.tagname])!=None:
            #         tagsname=request.POST[item.tagname]
            #         print(tagsname)
            #         b = tag.objects.get(tagname=tagsname)
            #         k = b.qcountintag
            #         a.tag_questions.add(b)
            #         b.qcountintag = k + 1
            #         b.save()
            a = questioncommit
            alltags=tag.objects.all()
            tags = request.POST.getlist('tags')
            for item in tags:
                b = tag.objects.get(tagname=item)
                k = b.qcountintag
                a.tag_questions.add(b)
                b.qcountintag = k + 1
                b.save()

            obj = User.objects.get(id=current_user.id)
            p = obj.point + 2
            obj.point = p
            obj.save()
            messages.info(request, '提交问题成功！')

            # 转到相关问题
            latestquestion = question.objects.latest('id')
            idnum = str(latestquestion.id)
            netstring = "http://127.0.0.1:8000/stack_under_flow/questioninfo/"
            return HttpResponseRedirect(netstring + idnum)
        except:
            messages.info(request, '提交问题失败！')

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    return render(request, 'stack_under_flow/commitquestion.html', locals())


def displayquestion(request):
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname
    question_list_obj = question.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 标签云
    tags_list_obj = tag.objects.all()

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    return render(request, 'stack_under_flow/displayquestion.html', locals())


def questioninfo(request, para):
    # 显示问题详情
    print(para)
    answer_list_obj = answer.objects.filter(questionid=para)

    # 判断用户名
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 点进详情后,阅读数目+1
    questioninfo = question.objects.get(id=para)
    viewcountpast = questioninfo.view
    questioninfo.view = viewcountpast + 1
    questioninfo.save()

    # 点击进入相关问题界面，消息已读
    read_message_count=message.objects.filter(message_questionid=para)
    for item in read_message_count:
        if current_user.nickname==item.receivemessage_usernickname:
            item.message_status='read'
            item.save()
        else:
            pass
    # 显示标签
    tagdisplay = questioninfo.tag_questions.all()

    # 提交用户回答
    if request.method == "POST":
        if current_user.is_authenticated:
            try:
                content = markdown(request.POST["content"], extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ])
                # 获取楼数
                ls = answer.objects.filter(questionid=para).count() + 1

                answercommit = answer()
                answercommit.content = content
                answercommit.contentstring = strip_tags(content)
                answercommit.userid = current_user.id
                answercommit.questionid = para
                answercommit.useridnickname = current_user.nickname
                answercommit.loushu = ls
                answercommit.save()
                obj = User.objects.get(id=current_user.id)
                p = obj.point + 1
                obj.point = p
                obj.save()
                now_anser = questioninfo.answercount
                questioninfo.answercount = now_anser + 1
                questioninfo.save()

                # 消息提醒功能
                new_message=message()
                new_message.sendmessage_usernickname=current_user.nickname
                new_message.receivemessage_usernickname=questioninfo.useridnickname
                new_message.message_content=strip_tags(content)
                new_message.message_questionid=questioninfo.id
                new_message.save()
                messages.info(request, '评论成功！')
            except:
                messages.info(request, '评论失败！请稍后再试一试吧！')
        else:
            messages.info(request, '请先登录再评论！')

    # dic_all=dict(dict_questioninfo.items()+answer_list_obj.ite)
    # 向bookInfo.html页面传入数据dict_book

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    return render(request, 'stack_under_flow/questioninfo.html', locals())


def itemsintag(request, para):
    print(para)

    # 显示用户名
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 标签云
    tags_list_obj = tag.objects.all()

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # 查询该标签下所有问题
    tagnamedisplay = tag.objects.get(id=para)
    tagsquestions = (tag.objects.get(id=para)).questions.all()
    return render(request, 'stack_under_flow/tag.html', locals())


def search(request):
    # --旧的disquestion代码:--
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 标签云
    tags_list_obj = tag.objects.all()

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # --旧的代码到此为止，看情况复用

    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'stack_under_flow/displayquestion.html', {'error_msg': error_msg})
    question_list_obj = question.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'stack_under_flow/displayquestion.html', locals())


def my(request):
    # --旧的disquestion代码:--
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # --旧的代码到此为止，看情况复用

    if current_user.is_anonymous:
        messages.info(request, '请登录后再查看自己的信息！')
        return HttpResponseRedirect('/')
    else:
        myquestions_list_obj = question.objects.filter(userid=current_user.id).order_by('-update_time')
        print(myquestions_list_obj)
    return render(request, 'stack_under_flow/my.html', locals())


def sendgiftpoint(request):
    def ErrorResponse3(message):
        data = {}
        data['status'] = 'ERROR'
        data['message'] = message
        return JsonResponse(data)

    def SuccessResponse3():
        data = {}
        data['status'] = 'SUCCESS'
        return JsonResponse(data)

    questionid = int(request.POST.get('questionid'))
    giftpoint = int(request.POST.get('giftpoint'))
    seeduserid = int(request.POST.get('seeduserid'))
    getuserid = int(request.POST.get('getuserid'))

    current_user = request.user
    if not current_user.is_authenticated:
        return ErrorResponse3('用户没有登陆！')
    if not current_user.id==seeduserid:
        return ErrorResponse3('用户不是题主！')

    # 发出悬赏的用户积分减去发出去的积分
    seeduser=User.objects.get(id=seeduserid)
    p1=seeduser.point
    if p1-giftpoint < 0:
        return ErrorResponse3('用户积分不够！')
    else:
        seeduser.point=p1-giftpoint
        seeduser.save()

    # 获得悬赏的用户积分加上发出去的积分
    getuser=User.objects.get(id=getuserid)
    p2=getuser.point
    getuser.point=p2+giftpoint
    getuser.save()

    # 问题悬赏分清零
    nowquestion=question.objects.get(id=questionid)
    nowquestion.giftpoint=0
    nowquestion.save()

    return SuccessResponse3()

def myadmin(request):
    # --旧的disquestion代码:--
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # --旧的代码到此为止，看情况复用
    if current_user.is_superuser:
        pass
    else:
        messages.info(request, '此页面只允许管理员进入')
        return HttpResponseRedirect('/')
    # 下面的是分页相关的
    # 分页显示：
    questiontable=question.objects.all().order_by('-update_time')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(questiontable, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        print(page)
        questiontable = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        questiontable = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        questiontable = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'stack_under_flow/myadmin.html', locals())

def searchtable(request):
    # --旧的disquestion代码:--
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # --旧的代码到此为止，看情况复用
    if current_user.is_superuser:
        pass
    else:
        messages.info(request, '此页面只允许管理员进入')
        return HttpResponseRedirect('/')

    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'stack_under_flow/myadmin.html', {'error_msg': error_msg})
    questiontable = question.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q) | Q(useridnickname__contains=q) | Q(
            update_time__contains=q)).order_by('-update_time')
    # 下面的是分页相关的
    # 分页显示：
    # questiontable=question.objects.all().order_by('-update_time')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(questiontable, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        print(page)
        questiontable = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        questiontable = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        questiontable = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'stack_under_flow/myadmin.html', locals())

def deletetable(request):
    def ErrorResponse4(message):
        data = {}
        data['status'] = 'ERROR'
        data['message'] = message
        return JsonResponse(data)

    def SuccessResponse4():
        data = {}
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    try:
        questionid = int(request.POST.get('questionid'))
        questiontodelete=question.objects.get(id=questionid)
        print("question的id值为:")
        print(questiontodelete.id)
        questiontodelete.delete()
        return SuccessResponse4()
    except:
        return ErrorResponse4('删除问题失败')
    # TODO 删帖功能完善，添加足够的信息

# TODO 信息提醒功能
def mynews(request):
    # --旧的disquestion代码:--
    current_user = request.user
    if current_user.is_anonymous:
        tempnickname = "游客"
    else:
        tempnickname = current_user.nickname

    # 传递标签
    tags_list_obj = tag.objects.all()

    # 显示最新问题
    newest_list_obj = question.objects.all().order_by('-update_time')

    # 显示最热门问题
    hotest_list_obj = question.objects.all().order_by('-view')

    # 显示最有价值的问题
    mostvalueable_list_obj = question.objects.all().order_by('-answercount')

    # 显示未读消息数目
    unread_message_count=message.objects.filter(receivemessage_usernickname=current_user.nickname,message_status='unread').count()

    # --旧的代码到此为止，看情况复用

    current_user.newscount=0
    current_user.save()
    # 下面的是分页相关的
    # 分页显示：
    mymessages = message.objects.filter(receivemessage_usernickname=current_user.nickname).order_by('-message_sendtime')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(mymessages, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        print(page)
        questiontable = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        questiontable = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        questiontable = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'stack_under_flow/mynews.html', locals())

def readallmessage(request):
    def ErrorResponse5(message):
        data = {}
        data['status'] = 'ERROR'
        data['message'] = message
        return JsonResponse(data)

    def SuccessResponse5():
        data = {}
        data['status'] = 'SUCCESS'
        return JsonResponse(data)

    try:
        current_usernickname = request.POST.get('current_usernickname')
        all_message_read=message.objects.filter(receivemessage_usernickname=current_usernickname)
        for item in all_message_read:
            item.message_status='read'
            item.save()
        return SuccessResponse5()
    except:
        return ErrorResponse5('阅读所有消息失败')
