# Generated by Django 5.0.6 on 2024-06-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_client_responsible'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='role_type',
            field=models.IntegerField(choices=[(1, 'Sênior'), (2, 'Assistente')], default=2),
            preserve_default=False,
        ),
    ]
