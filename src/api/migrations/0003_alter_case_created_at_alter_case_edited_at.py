# Generated by Django 4.1.5 on 2023-02-28 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_case_additional_time_alter_case_customer_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]