# Generated by Django 5.1.3 on 2024-11-25 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_token_token_created_alter_token_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='token_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.user'),
        ),
    ]
