# Generated by Django 3.0.3 on 2021-02-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210220_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='return_policy',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='viewcount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='warranty',
            field=models.CharField(max_length=100),
        ),
    ]
