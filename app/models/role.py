from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)
    remark = models.CharField(max_length=255)
    menus = models.ManyToManyField("Menu")

    @property
    def menu_permissions(self):
        return [m.identifier for m in self.menus.all()]
