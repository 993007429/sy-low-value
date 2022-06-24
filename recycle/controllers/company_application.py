from email.utils import formataddr

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from ninja import Router, Query
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from recycle.models.company_application import CompanyApplication, ApprovalState
from recycle.schemas.company_application import CompanyApplicationIn, CompanyApplicationOut, \
    CompanyApplicationOperationIn

router = Router(tags=["收运公司"])


@router.post("", response={201: None})
def submit_company_application(request, data: CompanyApplicationIn):
    """提交注册公司申请"""
    # FIXME: area_name改为根据code查询
    CompanyApplication.objects.create(**data.dict(), area_name=data.area_code)


@router.get("", response=Pagination[CompanyApplicationOut])
def list_company_applications(request,
                              state: ApprovalState = Query(None, title="审核状态"),
                              name: str = Query(None, title="公司名称"),
                              uniform_social_credit_code: str = Query(None, title="统一社会信用代码"),
                              page: Page = Query(...)):
    """查看清运公司审核列表"""

    queryset = CompanyApplication.objects.all().order_by("-id")
    if state:
        queryset = queryset.filter(state=state)
    if name:
        queryset = queryset.filter(name__contains=name)
    if uniform_social_credit_code:
        queryset = queryset.filter(uniform_social_credit_code=uniform_social_credit_code)
    paginator = Paginator(queryset, page.page_size)
    p = paginator.page(page.page)
    return {"count": paginator.count, "results": list(p.object_list)}


@router.patch("/{id_}", response=CompanyApplicationOut)
def update_company_application(request, id_: int, data: CompanyApplicationOperationIn):
    """清运公司审批"""

    with transaction.atomic():
        try:
            obj = CompanyApplication.objects.select_for_update().get(pk=id_, state=ApprovalState.APPROVING)
        except CompanyApplication.DoesNotExist:
            raise HttpError(404, "审批不存在或已审批完成")
        obj.state = data.state
        if data.state == ApprovalState.REJECTED:
            obj.reason = data.reason
        obj.save()

    # TODO: 生成随机密码
    password = "123456"
    # 发送邮件通知审核结果
    subject = "清运公司注册审核通知"
    if obj.state == ApprovalState.APPROVED:
        message = f"{obj.name} 审核通过。\n帐号：{obj.uniform_social_credit_code}\n密码：{password}"
    else:
        message = f"{obj.name} 审核未通过，原因：{obj.reason}"
    email_from = formataddr((settings.EMAIL_SENDER_NAME, settings.EMAIL_HOST_USER))
    recipient_list = [obj.manager_email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return obj
