# Generated by Django 3.1.2 on 2020-10-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oeta', '0004_auto_20201019_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='A', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]