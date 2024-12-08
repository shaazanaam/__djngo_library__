# Generated by Django 5.1.3 on 2024-12-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_bookinstance_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="language",
            field=models.ManyToManyField(
                help_text="Select languages for this book", to="catalog.language"
            ),
        ),
    ]