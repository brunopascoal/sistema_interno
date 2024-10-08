# Generated by Django 5.1 on 2024-09-24 20:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_is_approved'),
        ('assessments', '0009_evaluationschedule_commitment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='client',
        ),
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='commitment',
        ),
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='date_scheduled',
        ),
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='department',
        ),
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='other_commitment',
        ),
        migrations.RemoveField(
            model_name='evaluationschedule',
            name='role',
        ),
        migrations.AlterField(
            model_name='evaluationschedule',
            name='evaluatee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_scheduled', to=settings.AUTH_USER_MODEL, verbose_name='Avaliado'),
        ),
        migrations.AlterField(
            model_name='evaluationschedule',
            name='evaluator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation_schedules', to=settings.AUTH_USER_MODEL, verbose_name='Avaliador'),
        ),
        migrations.AlterField(
            model_name='evaluationschedule',
            name='self_evaluation',
            field=models.BooleanField(default=False, verbose_name='Autoavaliação'),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome do Trabalho')),
                ('date_scheduled', models.DateField(verbose_name='Data Agendada')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client', verbose_name='Cliente')),
                ('evaluatees', models.ManyToManyField(related_name='works_evaluatees', to=settings.AUTH_USER_MODEL, verbose_name='Avaliados')),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works_evaluator', to=settings.AUTH_USER_MODEL, verbose_name='Avaliador')),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works_responsible', to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
            ],
        ),
        migrations.AddField(
            model_name='evaluationschedule',
            name='work',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='assessments.work', verbose_name='Trabalho'),
            preserve_default=False,
        ),
    ]
