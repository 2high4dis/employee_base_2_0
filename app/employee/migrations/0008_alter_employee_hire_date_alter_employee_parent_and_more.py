# Generated by Django 4.2.8 on 2023-12-20 00:21

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_fill_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 12, 20))]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='employee.employee', verbose_name='Boss ID'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='post',
            field=models.CharField(choices=[('CEO', 'CEO'), ('D_CEO', 'Deputy CEO'), ('REG_MAN', 'Regional Manager'), ('TER_MAN', 'Territorial Manager'), ('DTER_MAN', 'Deputy Territorial Manager'), ('HON', 'Head of Network'), ('PHARM', 'Pharmacist')], default='PHARM', max_length=10),
        ),
    ]