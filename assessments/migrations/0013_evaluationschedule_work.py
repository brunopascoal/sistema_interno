# Generated by Django 5.1 on 2024-09-24 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0012_remove_evaluationschedule_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationschedule',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.work', verbose_name='Trabalho'),
        ),
    ]
