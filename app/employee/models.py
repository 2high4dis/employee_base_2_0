from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date
from django.core.validators import MaxValueValidator


class Employee(MPTTModel):
    class PostChoice(models.TextChoices):
        CEO = 'CEO', _('CEO')
        DEPUTY_CEO = 'D_CEO', _('Deputy CEO')
        REGIONAL_MANAGER = 'REG_MAN', _('Regional Manager')
        TERRITORIAL_MANAGER = 'TER_MAN', _('Territorial Manager')
        DEPUTY_TERRITORIAL_MANAGER = 'DTER_MAN', _(
            'Deputy Territorial Manager')
        HEAD_OF_NETWORK = 'HON', _('Head of Network')
        PHARMACIST = 'PHARM', _('Pharmacist')

    full_name = models.CharField(max_length=250)
    post = models.CharField(
        max_length=10, choices=PostChoice.choices, default=PostChoice.PHARMACIST)
    hire_date = models.DateField(
        validators=[MaxValueValidator(date.today)])
    parent = TreeForeignKey('self', on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='subordinates', verbose_name='boss ID')
    email = models.EmailField()

    def __str__(self):
        return f'{self.full_name}. ({self.get_post_display()})'

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['id']
