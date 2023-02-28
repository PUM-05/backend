# Generated by Django 4.1.5 on 2023-02-28 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='additional_time',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='customer_time',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='form_fill_time',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='medium',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='notes',
            field=models.TextField(null=True),
        ),
    ]
