# Generated by Django 4.1.7 on 2023-04-13 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_case_options_case_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'ordering': ['-created_at', '-id'], 'verbose_name_plural': 'cases'},
        ),
    ]
