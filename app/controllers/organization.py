from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from ninja import Router
from ninja.errors import HttpError

from app.models import Organization
from app.schemas.organization import OrganizationIn, OrganizationOut

router = Router(tags=["组织机构"])


@router.post("", response={201: OrganizationOut})
def create_organization(request, org_in: OrganizationIn):
    """创建组织机构"""

    exists = Organization.objects.filter(Q(name=org_in.name) | Q(code=org_in.code)).exists()
    if exists:
        raise HttpError(409, "机构名或编码已存在")
    if org_in.parent_id and not Organization.objects.filter(pk=org_in.parent_id).exists():
        raise HttpError(404, "上级机构不存在")
    organization = Organization.objects.create(**org_in.dict())
    return organization


@router.get("", response=List[OrganizationOut])
def list_organizations(request):
    """查询组织机构列表"""

    return Organization.objects.all()


@router.get("/{id_}", response=OrganizationOut)
def get_organizations(request, id_: int):
    """查看组织机构详情"""
    try:
        organization = Organization.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "组织机构不存在")
    return organization


@router.patch("/{id_}", response=OrganizationOut)
def patch_organization(request, id_: int, org_in: OrganizationIn):
    """修改组织机构"""

    try:
        organization = Organization.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "机构不存在")
    try:
        Organization.objects.get(pk=org_in.parent_id)
    except ObjectDoesNotExist:
        raise HttpError(404, "上级机构不存在")
    exists = (
        Organization.objects.exclude(pk=id_)
        .filter(Q(name=org_in.name) | (Q(code=org_in.code) & Q(code__isnull=False)))
        .exists()
    )
    if exists:
        raise HttpError(409, "机构名或编码已存在")

    for attr, value in org_in.dict().items():
        setattr(organization, attr, value)
    organization.save()
    return organization


@router.delete("/{id_}", response={204: None})
def delete_toilet_type(request, id_: int):
    try:
        toilet_type = Organization.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "机构不存在")
    toilet_type.delete()
    return None
