# Generated by Django 2.1.15 on 2021-05-02 07:41

from django.db import migrations
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_desc',
            field=mdeditor.fields.MDTextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
