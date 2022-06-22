"""组织机构"""
from ninja import Schema


class OrganizationBase(Schema):
    name: str
    code: str = None
    parent_id: int = None
    remark: str = None


class OrganizationIn(OrganizationBase):
    pass


class OrganizationOut(OrganizationBase):
    id: int
