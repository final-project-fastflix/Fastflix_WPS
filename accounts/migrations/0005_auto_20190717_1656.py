# Generated by Django 2.2.3 on 2019-07-17 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190717_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedislikemarked',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='likedislikemarked',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]