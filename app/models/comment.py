from django.contrib.postgres.fields import ArrayField
from django.db import models

from infra.db.models import BaseModel


class ToiletRatingEnum(models.IntegerChoices):
    SATISFIED = 3
    ACCEPTABLE = 2
    DISSATISFIED = 1


class ToiletComment(BaseModel):
    toilet = models.ForeignKey("Toilet", db_constraint=False, on_delete=models.CASCADE)
    ratings = models.SmallIntegerField("评价星级", choices=ToiletRatingEnum.choices)
    comment = models.CharField("评论内容", max_length=255, null=True, blank=True)
    user = models.ForeignKey("User", db_constraint=False, on_delete=models.SET_NULL, null=True, blank=True)
    photos = ArrayField(models.TextField(), default=list)
    anonymous = models.BooleanField("是否匿名", default=False)

    @property
    def toilet_name(self):
        return self.toilet.name

    @property
    def nickname(self):
        if self.user:
            if not self.anonymous:
                return self.user.nickname
            else:
                return "匿名"
        else:
            return None
