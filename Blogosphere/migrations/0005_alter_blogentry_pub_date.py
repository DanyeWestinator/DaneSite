# Generated by Django 4.0.1 on 2022-02-10 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogosphere', '0004_blogentry_docs_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='pub_date',
            field=models.DateField(null=True, verbose_name='Date Published'),
        ),
    ]