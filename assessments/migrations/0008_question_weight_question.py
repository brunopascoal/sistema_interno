# Generated by Django 5.1 on 2024-09-11 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0007_evaluation_role_at_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='weight_question',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
            preserve_default=False,
        ),
    ]