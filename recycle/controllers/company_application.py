from email.utils import formataddr

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from ninja import Query, Router
from ninja.errors import HttpError

from infra.schemas import Page, Pagination
from recycle.models import Company, CompanyManager, User
from recycle.models.company_application import ApprovalState, CompanyApplication
from recycle.schemas.company_application import (
    CompanyApplicationIn,
    CompanyApplicationOperationIn,
    CompanyApplicationOut,
)

router = Router(tags=["收运公司"])


@router.post("", response={201: None})
def submit_company_application(request, data: CompanyApplicationIn):
    """提交注册公司申请"""
    # FIXME: area_name改为根据code查询
    CompanyApplication.objects.create(**data.dict(), area_name=data.area_code)


@router.get("", response=Pagination[CompanyApplicationOut])
def list_company_applications(
        request,
        state: ApprovalState = Query(None, title="审核状态"),
        name: str = Query(None, title="公司名称"),
        uniform_social_credit_code: str = Query(None, title="统一社会信用代码"),
        page: Page = Query(...),
):
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
            obj: CompanyApplication = CompanyApplication.objects.select_for_update().get(
                pk=id_, state=ApprovalState.APPROVING
            )
        except CompanyApplication.DoesNotExist:
            raise HttpError(404, "审批不存在或已审批完成")
        obj.state = data.state
        if data.state == ApprovalState.REJECTED:
            obj.reason = data.reason
        obj.save()

        password = User.objects.make_random_password()
        if obj.state == ApprovalState.APPROVED:
            # 创建公司管理员帐号
            user = User.objects.create_user(
                username=obj.uniform_social_credit_code,
                email=obj.manager_email,
                password=password,
            )
            manager = CompanyManager.objects.create(
                user=user,
                name=obj.manager_name,
                id_card=obj.manager_id_card,
                phone=obj.manager_phone,
                email=obj.manager_email,
                address=obj.manager_address,
                id_card_front=obj.manager_id_card_front,
                id_card_back=obj.manager_id_card_back,
            )
            # 创建公司, TODO: 验证各种字段唯一性
            Company.objects.create(
                name=obj.name,
                uniform_social_credit_code=obj.uniform_social_credit_code,
                address=obj.address,
                area_code=obj.area_code,
                area_name=obj.area_name,
                form=obj.form,
                legal_person=obj.legal_person,
                legal_person_id_card=obj.legal_person_id_card,
                business_license=obj.business_license,
                qualification=obj.qualification,
                manager=manager,
            )
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
