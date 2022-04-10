# Generated by Django 4.0.3 on 2022-04-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_alter_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followed',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='rest_api.userprofile'),
        ),
    ]
