from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord
from .models import UnLikeCount,UnLikeRecord
from django.contrib import messages


def ErrorResponse1(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SuccessResponse1(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)


def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse1(400, '你没有登陆！')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
    except ObjectDoesNotExist:
        return ErrorResponse1(401, '对象不存在！')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse1(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse1(402, '不能重复点赞！')
    else:
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse1(like_count.liked_num)
            else:
                return ErrorResponse1(404, '数据错误，请稍后重试')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse1(403, '你没有赞过，不能取消')


def ErrorResponse2(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SuccessResponse2(unliked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['unliked_num'] = unliked_num
    return JsonResponse(data)


def unlike_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse2(400, '你没有登陆！')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse2(401, '对象不存在！')

    # 处理数据
    if request.GET.get('is_unlike') == 'true':
        # 要点踩
        unlike_record, created = UnLikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
        # 未踩过，进行踩
            unlike_count, created = UnLikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            unlike_count.unliked_num += 1
            unlike_count.save()
            return SuccessResponse2(unlike_count.unliked_num)
        else:
            # 已踩过，不能重复踩
            return ErrorResponse2(402, '不能重复踩！')
    else:
        # 要取消点赞
        if UnLikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            unlike_record = UnLikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            unlike_record.delete()
            # 点赞总数减1
            unlike_count, created = UnLikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                unlike_count.unliked_num -= 1
                unlike_count.save()
                return SuccessResponse2(unlike_count.unliked_num)
            else:
                return ErrorResponse2(404, '数据错误！')
        else:
            # 没有点踩过，不能取消
            return ErrorResponse2(403, '你没有踩过！')
