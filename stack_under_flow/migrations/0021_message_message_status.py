# Generated by Django 2.0.6 on 2018-06-24 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_under_flow', '0020_message_message_questionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_status',
            field=models.CharField(default='unread', max_length=500),
        ),
    ]
