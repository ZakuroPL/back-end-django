# Generated by Django 3.1 on 2020-12-21 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('picture', models.CharField(max_length=128)),
                ('link', models.CharField(max_length=128)),
                ('match', models.IntegerField(default=0)),
                ('isPremium', models.BooleanField(default=False)),
                ('inch', models.IntegerField()),
                ('isOled', models.BooleanField(default=False)),
                ('isFullArray', models.BooleanField(default=False)),
                ('is100hz', models.BooleanField(default=False)),
                ('is10bit', models.BooleanField(default=False)),
                ('isDolbyVision', models.BooleanField(default=False)),
                ('isVoiceControl', models.BooleanField(default=False)),
                ('isNetflix', models.BooleanField(default=True)),
                ('isYouTube', models.BooleanField(default=True)),
                ('isHboGo', models.BooleanField(default=False)),
                ('isRakuten', models.BooleanField(default=False)),
                ('isPrimeVideo', models.BooleanField(default=False)),
                ('isAppleTv', models.BooleanField(default=False)),
                ('isPlayer', models.BooleanField(default=False)),
                ('isIpla', models.BooleanField(default=False)),
            ],
        ),
    ]