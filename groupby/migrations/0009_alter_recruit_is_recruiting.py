# Generated by Django 4.0.5 on 2022-08-16 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupby', '0008_alter_recruit_is_recruiting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='is_recruiting',
            field=models.CharField(choices=[('ing', '채용중'), ('end', '채용마감')], max_length=200),
        ),
    ]
