# Generated by Django 3.2.3 on 2021-06-06 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_auto_20210530_1634"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="likes",
            new_name="claps",
        ),
    ]
