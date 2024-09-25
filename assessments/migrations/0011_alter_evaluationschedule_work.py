# Generated by Django 5.1 on 2024-09-24 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0010_remove_evaluationschedule_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationschedule',
            name='work',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.work', verbose_name='Trabalho'),
        ),
        migrations.AddField(
            model_name='evaluationschedule',
            name='work',
            field=models.ForeignKey(
                default=1,  # Defina um ID válido de Work aqui
                to='assessments.Work',
                on_delete=models.CASCADE,
                verbose_name='Trabalho'
            ),
            preserve_default=False,
)
    ]