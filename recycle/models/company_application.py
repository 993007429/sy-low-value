from django.db import models

from infra.db.models import BaseModel


class ApprovalState(models.TextChoices):
    APPROVING = "APPROVING", "审核中"
    APPROVED = "APPROVED", "审核通过"
    REJECTED = "REJECTED", "审核拒绝"


class CompanyApplication(BaseModel):
    """清运公司注册申请"""

    # 公司信息
    name = models.CharField("公司名称", max_length=255)
    uniform_social_credit_code = models.CharField("统一社会信用代码", max_length=32)
    address = models.CharField("公司地址", max_length=255)
    area_code = models.CharField("注册区编码", max_length=32)
    area_name = models.CharField("注册区名称", max_length=32)
    form = models.CharField("企业类型", max_length=32)
    legal_person = models.CharField("法人", max_length=32)
    legal_person_id_card = models.CharField("法人身份证", max_length=32)
    business_license = models.CharField("营业执照", max_length=512)
    qualification = models.CharField("资质", max_length=512)

    # 负责人信息
    manager_name = models.CharField("姓名", max_length=32)
    manager_id_card = models.CharField("身份证", max_length=32)
    manager_phone = models.CharField("联系电话", max_length=32)
    manager_email = models.EmailField()
    manager_address = models.CharField("居住地址", max_length=255)
    manager_id_card_front = models.CharField("身份证正面", max_length=255)
    manager_id_card_back = models.CharField("身份证背面", max_length=255)

    # 审核状态
    state = models.CharField("审核状态", max_length=32, choices=ApprovalState.choices, default=ApprovalState.APPROVING)
    # 审核拒绝原因(仅在拒绝时有效)
    reason = models.CharField("审核拒绝原因", max_length=255, null=True, blank=True)
