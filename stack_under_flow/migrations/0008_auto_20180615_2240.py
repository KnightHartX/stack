# Generated by Django 2.0.6 on 2018-06-15 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_under_flow', '0007_auto_20180614_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(max_length=5000),
        ),
    ]
