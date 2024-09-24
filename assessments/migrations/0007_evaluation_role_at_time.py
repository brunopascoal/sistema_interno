# Generated by Django 5.1 on 2024-09-04 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_role_role_type'),
        ('assessments', '0006_evaluationschedule_self_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='role_at_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.role'),
        ),
    ]