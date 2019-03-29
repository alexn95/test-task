# Generated by Django 2.1.5 on 2019-03-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_name', models.CharField(blank=True, max_length=100)),
                ('data_file', models.FileField(upload_to='data')),
            ],
        ),
    ]
