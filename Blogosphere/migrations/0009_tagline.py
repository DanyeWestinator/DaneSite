# Generated by Django 4.0.1 on 2022-02-11 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogosphere', '0008_alter_blogentry_blog_tags_alter_blogentry_blog_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.TextField(blank=True, null=True, verbose_name='Tagline')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date added')),
            ],
        ),
    ]
