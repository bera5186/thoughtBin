# Generated by Django 3.2.3 on 2021-05-29 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_comment_author_reply"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="author_reply",
            field=models.TextField(default="", max_length=1000),
        ),
    ]
