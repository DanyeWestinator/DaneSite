# Generated by Django 4.0.1 on 2022-02-03 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogosphere', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentry',
            name='plain_text',
            field=models.TextField(default='', verbose_name='Plain Text'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='num_words',
            field=models.IntegerField(verbose_name='Number of Words'),
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='text_body',
            field=models.TextField(verbose_name='Raw HTML'),
        ),
    ]
