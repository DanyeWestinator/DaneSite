# Generated by Django 4.0.1 on 2022-02-17 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogosphere', '0009_tagline'),
    ]

    operations = [
        migrations.CreateModel(
            name='RandomDaneFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fact', models.TextField(blank=True, null=True, verbose_name='Fact: ')),
                ('source', models.TextField(blank=True, null=True, verbose_name='Source link')),
            ],
        ),
    ]
