from typing import List

from django.core.exceptions import ObjectDoesNotExist
from ninja import Router
from ninja.errors import HttpError

from app.models.toliet_type import ToiletType
from app.schemas.toliet_type import ToiletTypeIn, ToiletTypeOut

router = Router(tags=["公厕类型"])


@router.post("", response={201: ToiletTypeOut})
def create_toilet_type(request, toilet_type_in: ToiletTypeIn):
    """创建公厕类型"""
    exists = ToiletType.objects.filter(name=toilet_type_in.name).exists()
    if exists:
        raise HttpError(409, "公厕类型已存在")
    else:
        toilet_type = ToiletType.objects.create(name=toilet_type_in.name)
        return toilet_type


@router.get("", response=List[ToiletTypeOut])
def list_toilet_types(request):
    """查询公厕类型"""
    return ToiletType.objects.all()


@router.patch("/{id_}", response=ToiletTypeOut)
def patch_toilet_type(request, id_: int, toilet_type_in: ToiletTypeIn):
    try:
        toilet_type = ToiletType.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕类型不存在")

    exists = ToiletType.objects.exclude(pk=id_).filter(name=toilet_type_in.name).exists()
    if exists:
        raise HttpError(409, "公厕类型已存在")
    toilet_type.name = toilet_type_in.name
    toilet_type.save()
    return toilet_type


@router.delete("/{id_}", response={204: None})
def delete_toilet_type(request, id_: int):
    try:
        toilet_type = ToiletType.objects.get(pk=id_)
    except ObjectDoesNotExist:
        raise HttpError(404, "公厕类型不存在")
    toilet_type.delete()
    return None
