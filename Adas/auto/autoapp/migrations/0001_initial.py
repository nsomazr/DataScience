# Generated by Django 2.1.1 on 2018-09-20 22:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='auto_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('uname', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='cleanData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepaths_clean', models.FileField(max_length=200, upload_to='E:\\Google\\Telesoft\\Telegrammer\\PycharmProjects\\Adas\\auto\\filepaths_clean')),
                ('filename_clean', models.CharField(max_length=50)),
                ('clean_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoapp.auto_users')),
            ],
        ),
        migrations.CreateModel(
            name='upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepaths', models.FileField(max_length=200, upload_to='E:\\Google\\Telesoft\\Telegrammer\\PycharmProjects\\Adas\\auto\\filepaths')),
                ('filename', models.CharField(max_length=50)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoapp.auto_users')),
            ],
        ),
    ]
