from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from ninja import Query, Router
from ninja.errors import HttpError

from app.models import Toilet
from app.models.comment import ToiletComment
from app.schemas import Pagination
from app.schemas.toilet_comment import ToiletCommentIn, ToiletCommentOut, ToiletUserCommentIn
from infra.authentication import terminal_auth

router = Router(tags=["公厕评论"])


@router.post("", response={201: ToiletCommentOut}, auth=terminal_auth)
def create_toilet_comment(request, toilet_comment_in: ToiletCommentIn):
    toilet = request.auth
    toilet_comment = ToiletComment.objects.create(
        toilet=toilet, ratings=toilet_comment_in.ratings, comment=toilet_comment_in.comment
    )
    return toilet_comment


@router.post("/user", response={201: ToiletCommentOut})
def create_toilet_comment_user(request, toilet_comment_in: ToiletUserCommentIn):
    try:
        toilet = Toilet.objects.get(terminal_id=toilet_comment_in.terminal_id)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕不存在")

    toilet_comment = ToiletComment.objects.create(
        toilet=toilet,
        ratings=toilet_comment_in.ratings,
        comment=toilet_comment_in.comment,
        photos=toilet_comment_in.photos,
        anonymous=toilet_comment_in.anonymous,
        user=request.auth,
    )
    return toilet_comment


@router.get("", response=Pagination[ToiletCommentOut])
def list_toilet_comments(
    request,
    start_time: datetime = None,
    end_time: datetime = None,
    terminal_id: str = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, le=100, ge=1),
    user_id: int = None,
):
    queryset = ToiletComment.objects.all().prefetch_related("toilet", "user").order_by("-created_at")
    if terminal_id:
        queryset = queryset.filter(toilet__terminal_id=terminal_id)
    if start_time:
        queryset = queryset.filter(created_at__gte=start_time)
    if end_time:
        queryset = queryset.filter(created_at__lte=end_time)
    if user_id:
        queryset = queryset.filter(user_id=user_id)
    paginator = Paginator(queryset, page_size)
    p = paginator.page(page)
    return {"count": paginator.count, "results": list(p.object_list)}
