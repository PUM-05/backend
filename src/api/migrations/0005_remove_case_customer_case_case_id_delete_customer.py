# Generated by Django 4.1.7 on 2023-04-16 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_case_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='customer',
        ),
        migrations.AddField(
            model_name='case',
            name='case_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
