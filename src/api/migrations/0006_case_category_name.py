# Generated by Django 4.1.7 on 2023-04-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_case_customer_case_case_id_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='category_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]