# Generated by Django 2.0.6 on 2018-06-17 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_under_flow', '0011_auto_20180617_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(max_length=500)),
                ('questions', models.ManyToManyField(to='stack_under_flow.question')),
            ],
        ),
    ]
