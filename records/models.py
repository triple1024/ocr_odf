from django.db import models

class Address(models.Model):
    date = models.DateField(verbose_name="日付")
    name = models.CharField(max_length=100, verbose_name='従業員名')
    department = models.CharField(max_length=100, verbose_name='部署')

    class Meta:
        verbose_name_plural = '住所変更届'

    def __str__(self):
        return self.name