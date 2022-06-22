from django.db import models

from infra.db.models import BaseModel


class Organization(BaseModel):
    """组织机构"""

    name = models.CharField("组织名", max_length=128, unique=True)
    code = models.CharField("组织编码", max_length=64, unique=True, null=True, blank=True)
    parent = models.ForeignKey(
        verbose_name="上级组织",
        to="Organization",
        on_delete=models.RESTRICT,
        related_name="children",
        db_constraint=False,
        blank=True,
        null=True,
    )
    remark = models.CharField("备注", max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name
